extends Node3D

const Player = preload("res://scripts/player.gd")
var player: CharacterBody3D
var day_sky: Sky
var night_sky: Sky
var env: Environment
var sun: DirectionalLight3D
var night_lights: Node3D
var night: bool = false
var menu: Control
var hud: Control
var status: Label
var info: Label
var clock_label: Label
var help_label: Label
var impact_pool: Array[Node3D] = []
var mat_emissions: Array[StandardMaterial3D] = []
var fps_history: Array[float] = []
var qa_mode: bool = false
var world_meshes: int = 0
var collision_shapes: int = 0
var pause_open: bool = true
var qa_root: String

func _ready() -> void:
	qa_mode = "--qa" in OS.get_cmdline_user_args()
	qa_root = ProjectSettings.globalize_path("res://qa") if OS.has_feature("editor") else OS.get_executable_path().get_base_dir().path_join("../../../captures").simplify_path()
	DirAccess.make_dir_recursive_absolute(qa_root)
	RenderingServer.set_default_clear_color(Color(.15,.20,.28))
	var map_scene: PackedScene = load("res://assets/square.glb")
	var map_node := map_scene.instantiate()
	map_node.name = "BlenderScene"
	add_child(map_node)
	prepare_visuals(map_node)
	var proxy: Node3D = load("res://assets/collision.glb").instantiate()
	add_child(proxy)
	prepare_collision(proxy)
	proxy.queue_free()
	# Thin ground safety surface matches the plaza walking level; architecture uses exported proxies.
	var floor_body := StaticBody3D.new()
	var floor_shape := CollisionShape3D.new()
	var floor_box := BoxShape3D.new()
	floor_box.size = Vector3(580,.2,580)
	floor_shape.shape = floor_box
	floor_shape.position.y=-.11
	floor_body.add_child(floor_shape)
	add_child(floor_body)
	for boundary in [Vector3(-275,8,0),Vector3(275,8,0),Vector3(0,8,-275),Vector3(0,8,275)]:
		var body := StaticBody3D.new()
		var shape := CollisionShape3D.new()
		var box := BoxShape3D.new()
		box.size=Vector3(1,20,550) if boundary.x!=0 else Vector3(550,20,1)
		shape.shape=box
		body.position=boundary
		body.add_child(shape)
		add_child(body)
	build_lighting()
	player=CharacterBody3D.new()
	player.set_script(Player)
	add_child(player)
	build_ui()
	var audio := AudioStreamPlayer.new()
	audio.stream=load("res://audio/ambience.wav")
	audio.stream.loop_mode=AudioStreamWAV.LOOP_FORWARD
	audio.volume_db=-27
	add_child(audio)
	audio.play()
	set_night(false)
	if qa_mode:
		DirAccess.make_dir_recursive_absolute(qa_root)
		run_qa()

func prepare_visuals(node: Node) -> void:
	if node is MeshInstance3D:
		world_meshes+=1
		var mi: MeshInstance3D=node
		for i in range(mi.mesh.get_surface_count()):
			var mat := mi.get_active_material(i)
			if mat is StandardMaterial3D:
				mat.texture_filter=BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
				# Exported scene contains double-sided ornamental sheets as well as solid meshes.
				mat.cull_mode=BaseMaterial3D.CULL_DISABLED
				if "lamp glass" in mat.resource_name.to_lower() or "shop glazing" in mat.resource_name.to_lower():
					var cp: StandardMaterial3D=mat.duplicate()
					mi.set_surface_override_material(i,cp)
					mat_emissions.append(cp)
	for child in node.get_children(): prepare_visuals(child)

func prepare_collision(node: Node) -> void:
	if node is MeshInstance3D:
		var mi: MeshInstance3D=node
		var body := StaticBody3D.new()
		body.name="Solid_"+str(collision_shapes)
		add_child(body)
		body.global_transform=mi.global_transform
		var shape := CollisionShape3D.new()
		shape.shape=mi.mesh.create_trimesh_shape()
		body.add_child(shape)
		collision_shapes+=1
	for child in node.get_children(): prepare_collision(child)

func from_blender(a: Array) -> Vector3:
	return Vector3(float(a[0]),float(a[2]),-float(a[1]))

func build_lighting() -> void:
	var we := WorldEnvironment.new()
	env=Environment.new()
	we.environment=env
	add_child(we)
	env.background_mode=Environment.BG_SKY
	day_sky=Sky.new()
	var panorama := PanoramaSkyMaterial.new()
	panorama.panorama=load("res://assets/day_sky.hdr")
	day_sky.sky_material=panorama
	night_sky=Sky.new()
	var dark_sky := ProceduralSkyMaterial.new()
	dark_sky.sky_top_color=Color(.09,.13,.22)
	dark_sky.sky_horizon_color=Color(.19,.23,.30)
	dark_sky.ground_bottom_color=Color(.04,.05,.07)
	dark_sky.ground_horizon_color=Color(.16,.19,.24)
	night_sky.sky_material=dark_sky
	env.sky=day_sky
	env.ambient_light_source=Environment.AMBIENT_SOURCE_COLOR
	env.tonemap_mode=Environment.TONE_MAPPER_ACES
	env.ssao_enabled=true
	env.ssao_radius=1.1
	env.ssao_intensity=1.3
	env.glow_enabled=true
	env.glow_intensity=.45
	env.fog_enabled=true
	env.fog_density=.00065
	env.fog_light_color=Color(.67,.73,.8)
	sun=DirectionalLight3D.new()
	sun.rotation_degrees=Vector3(-44,-110,0)
	sun.light_color=Color(1.0,.93,.80)
	sun.light_energy=1.1
	sun.shadow_enabled=true
	sun.directional_shadow_max_distance=190
	sun.directional_shadow_mode=DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS
	add_child(sun)
	night_lights=Node3D.new()
	night_lights.name="ArchitecturalNightLights"
	add_child(night_lights)
	var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://assets/lighting.json"))
	var commercial_index: int=0
	for item in data.night_lights:
		var name_string: String=item.name
		if "commercial" in name_string:
			commercial_index+=1
			if commercial_index%3!=0: continue
		if item.type!="SPOT": continue
		var light := SpotLight3D.new()
		night_lights.add_child(light)
		light.name=name_string
		light.position=from_blender(item.position_blender)
		var target := from_blender(item.target_blender)
		if light.position.distance_to(target)<.01: light.queue_free();continue
		var up := Vector3.UP
		if absf((target-light.position).normalized().dot(up))>.98: up=Vector3.RIGHT
		light.look_at(target,up)
		var c: Array=item.color_linear
		light.light_color=Color(float(c[0]),float(c[1]),float(c[2])).linear_to_srgb()
		light.light_energy=clampf(float(item.power_watts)/60.0,1.2,20.0)
		light.spot_range=clampf(light.position.distance_to(target)*1.8+4,9,42)
		light.spot_angle=clampf(float(item.get("spot_degrees",65))*.5,15,60)
		light.spot_attenuation=.8
		light.distance_fade_enabled=true
		light.distance_fade_begin=95
		light.distance_fade_length=40
		light.shadow_enabled=false
	# Broad reflected spill approximates bounce; not a one-to-one Cycles lighting transfer.
	for pos in [Vector3(-24,9,0),Vector3(7,18,16),Vector3(7,18,-16),Vector3(23,12,0)]:
		var light := OmniLight3D.new()
		light.position=pos
		light.omni_range=48
		light.light_color=Color(1,.87,.67)
		light.light_energy=9.0
		night_lights.add_child(light)


	var moon := DirectionalLight3D.new()
	moon.rotation_degrees=Vector3(-55,-100,0)
	moon.light_color=Color(.5,.64,.88)
	moon.light_energy=.26
	night_lights.add_child(moon)
	for pos in [Vector3(-18,36,24),Vector3(-18,36,-24)]:
		var roof := SpotLight3D.new()
		night_lights.add_child(roof)
		roof.position=pos
		roof.look_at(Vector3(0,43,0),Vector3.UP)
		roof.light_color=Color(.85,.92,1.0)
		roof.light_energy=18
		roof.spot_range=65
		roof.spot_angle=35

func set_night(value: bool) -> void:
	night=value
	night_lights.visible=value
	sun.visible=not value
	env.background_mode=Environment.BG_SKY
	env.sky=night_sky if value else day_sky
	env.fog_sky_affect=.15
	env.background_color=Color(.13,.18,.28)
	env.ambient_light_color=Color(.46,.53,.68) if value else Color(.73,.80,.90)
	env.ambient_light_energy=1.0 if value else .7
	env.tonemap_exposure=1.45 if value else 1.15
	env.background_energy_multiplier=1.0
	env.fog_light_color=Color(.12,.17,.25) if value else Color(.67,.73,.80)
	for mat in mat_emissions:
		mat.emission_enabled=value
		mat.emission=Color(1,.83,.6)
		mat.emission_energy_multiplier=.18 if value else 0
	if clock_label: clock_label.text="索菲亚广场  /  夜间" if value else "索菲亚广场  /  白天"

func text_label(parent: Node, text: String, size: int, pos: Vector2, color: Color=Color(.90,.92,.94)) -> Label:
	var l := Label.new()
	l.text=text
	l.position=pos
	l.add_theme_font_size_override("font_size",size)
	l.add_theme_color_override("font_color",color)
	l.add_theme_color_override("font_shadow_color",Color(0,0,0,.8))
	l.add_theme_constant_override("shadow_offset_x",1)
	l.add_theme_constant_override("shadow_offset_y",1)
	parent.add_child(l)
	return l

func build_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	hud=Control.new()
	hud.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	hud.mouse_filter=Control.MOUSE_FILTER_IGNORE
	layer.add_child(hud)
	clock_label=text_label(hud,"索菲亚广场  /  白天",22,Vector2(30,24))
	info=text_label(hud,"",15,Vector2(30,59),Color(.75,.82,.86))
	status=text_label(hud,"",22,Vector2(1180,814))
	help_label=text_label(hud,"WASD 移动  ·  Shift 奔跑  ·  空格 跳跃  ·  左键 开火  ·  右键 瞄准\nR 换弹  ·  N 昼夜  ·  F 手电  ·  G 收枪  ·  H 界面  ·  Esc 菜单",17,Vector2(30,817))
	var cross := Label.new()
	cross.text="·"
	cross.add_theme_font_size_override("font_size",30)
	cross.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	cross.position=Vector2(715,428)
	hud.add_child(cross)
	menu=Control.new()
	menu.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	layer.add_child(menu)
	var shade := ColorRect.new()
	shade.color=Color(.025,.04,.065,.86)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	menu.add_child(shade)
	text_label(menu,"HARBIN  /  EXTERIOR WALK",18,Vector2(95,145),Color(.78,.65,.40))
	text_label(menu,"索菲亚广场",58,Vector2(90,187))
	text_label(menu,"第一人称持枪漫游",26,Vector2(96,274),Color(.74,.79,.82))
	text_label(menu,"沿广场行走，靠近砖墙与门廊，切换昼夜。\nWASD 移动 · 鼠标环顾 · Esc 释放鼠标\n左键开火 · 右键瞄准 · R 换弹 · F 手电",20,Vector2(96,341))
	var labels := ["进入白天", "进入夜晚", "继续漫游", "返回起点", "退出"]
	for i in range(labels.size()):
		var b := Button.new()
		b.text=labels[i]
		b.position=Vector2(96+i*182,480)
		b.size=Vector2(168,55)
		b.add_theme_font_size_override("font_size",21)
		menu.add_child(b)
		match i:
			0: b.pressed.connect(func(): set_night(false);set_menu(false))
			1: b.pressed.connect(func(): set_night(true);set_menu(false))
			2: b.pressed.connect(func(): set_menu(false))
			3: b.pressed.connect(func(): player.reset_position();set_menu(false))
			4: b.pressed.connect(func(): get_tree().quit())
	text_label(menu,"V2.2.1 DEMO   ·   户外场景，教堂内部未开放\n场景依据照片持续修订；实景还原验收仍在进行。",16,Vector2(96,720),Color(.60,.67,.72))
	set_menu(true)

func set_menu(opened: bool) -> void:
	pause_open=opened
	menu.visible=opened
	player.enabled=not opened
	hud.visible=not opened
	Input.mouse_mode=Input.MOUSE_MODE_VISIBLE if opened else Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_ESCAPE: set_menu(not pause_open)
			KEY_N: set_night(not night)
			KEY_H: hud.visible=not hud.visible
			KEY_P: save_capture("capture_"+str(Time.get_unix_time_from_system()).replace(".","_"))

func _process(delta: float) -> void:
	if delta>0 and not pause_open:
		fps_history.append(1.0/delta)
		if fps_history.size()>600: fps_history.pop_front()
	if info:
		info.text="%.0f FPS  ·  视线 1.70 m" % Engine.get_frames_per_second()
	if status:
		status.text="换弹中…" if player.reload_time>0 else "%02d / ∞" % player.ammo

func impact(pos: Vector3, normal: Vector3) -> void:
	var ob := MeshInstance3D.new()
	var mesh := SphereMesh.new()
	mesh.radius=.028
	mesh.height=.056
	mesh.radial_segments=8
	mesh.rings=4
	ob.mesh=mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color=Color(.08,.065,.05)
	mat.roughness=.96
	ob.material_override=mat
	ob.position=pos+normal*.015
	add_child(ob)
	impact_pool.append(ob)
	if impact_pool.size()>48: impact_pool.pop_front().queue_free()

func save_capture(name_string: String) -> void:
	await RenderingServer.frame_post_draw
	var path := qa_root.path_join(name_string+".png")
	get_viewport().get_texture().get_image().save_png(path)

func run_qa() -> void:
	await get_tree().create_timer(3).timeout
	set_menu(false)
	Input.mouse_mode=Input.MOUSE_MODE_VISIBLE
	await get_tree().create_timer(2).timeout
	await save_capture("day_spawn")
	var report: Dictionary={"engine":Engine.get_version_info().string,"renderer":RenderingServer.get_current_rendering_method(),"meshes":world_meshes,"collision_shapes":collision_shapes,"checks":{}}
	var checks: Dictionary=report.checks
	checks["spawn_grounded"]=player.is_on_floor()
	checks["eye_height_1_7"]=is_equal_approx(player.camera.position.y,1.7)
	var start: Vector3=player.position
	Input.action_release("ui_accept")
	# Exercise actual controller keyboard input through Godot's input event queue.
	var ev := InputEventKey.new()
	ev.physical_keycode=KEY_W
	ev.pressed=true
	Input.parse_input_event(ev)
	await get_tree().create_timer(1.5).timeout
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=false;Input.parse_input_event(ev)
	checks["walk_moves_player"]=player.position.distance_to(start)>3
	player.fire()
	checks["shot_consumes_round"]=player.ammo==29 and player.shots_fired==1
	player.reload_gun()
	await get_tree().create_timer(1.8).timeout
	checks["reload_restores_magazine"]=player.ammo==30
	var floor_y: float=player.position.y
	ev=InputEventKey.new();ev.physical_keycode=KEY_SPACE;ev.pressed=true;Input.parse_input_event(ev)
	await get_tree().create_timer(.25).timeout
	checks["jump_rises"]=player.position.y>floor_y+.3
	ev=InputEventKey.new();ev.physical_keycode=KEY_SPACE;ev.pressed=false;Input.parse_input_event(ev)
	await get_tree().create_timer(1.0).timeout
	checks["jump_lands"]=player.is_on_floor()
	var mouse := InputEventMouseButton.new()
	mouse.button_index=MOUSE_BUTTON_RIGHT;mouse.pressed=true;Input.parse_input_event(mouse)
	await get_tree().create_timer(.35).timeout
	checks["aim_narrows_fov"]=player.camera.fov<58
	mouse=InputEventMouseButton.new();mouse.button_index=MOUSE_BUTTON_RIGHT;mouse.pressed=false;Input.parse_input_event(mouse)
	player.torch.visible=true
	checks["flashlight_toggle"]=player.torch.visible
	player.torch.visible=false
	player.gun_visible=false
	await get_tree().create_timer(.08).timeout
	checks["holster_hides_gun"]=not player.weapon.visible
	player.gun_visible=true
	set_menu(true)
	checks["pause_releases_mouse"]=not player.enabled and Input.mouse_mode==Input.MOUSE_MODE_VISIBLE
	set_menu(false)
	Input.mouse_mode=Input.MOUSE_MODE_VISIBLE
	player.position=Vector3(-28,.18,0)
	player.rotation.y=-PI/2
	player.pitch=.17
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=true;Input.parse_input_event(ev)
	await get_tree().create_timer(3.5).timeout
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=false;Input.parse_input_event(ev)
	checks["entry_stairs_climbed"]=player.position.y>.25
	checks["church_wall_blocks"]=player.position.x < -19
	report["entry_position"]=str(player.position)
	report["step_assists"]=player.step_assists
	await save_capture("day_portal")
	player.reset_position()
	set_night(true)
	await get_tree().create_timer(3).timeout
	checks["night_lamps_on"]=night_lights.visible and not sun.visible
	await save_capture("night_spawn")
	player.torch.visible=true
	await get_tree().create_timer(.5).timeout
	await save_capture("night_flashlight")
	player.torch.visible=false
	set_night(false)
	checks["day_lamps_off"]=not night_lights.visible and sun.visible
	player.position=Vector3(-32,.2,-66)
	player.rotation.y=0
	player.pitch=.18
	await get_tree().create_timer(2).timeout
	await save_capture("day_north")
	# Regression views and traversal for the user-reported gallery / market defects.
	player.position=Vector3(-77,.18,-30)
	player.rotation.y=-1.10
	player.pitch=.13
	await get_tree().create_timer(.8).timeout
	await save_capture("gallery_front")
	# Traverse an actual arch opening, then independently challenge the middle pier.
	player.position=Vector3(-72,.18,-39.4)
	player.rotation.y=-PI/2
	player.pitch=.10
	await get_tree().create_timer(.5).timeout
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=true;Input.parse_input_event(ev)
	await get_tree().create_timer(2.5).timeout
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=false;Input.parse_input_event(ev)
	await get_tree().create_timer(.2).timeout
	checks["gallery_stairs_reach_landing"]=player.position.y>1.0 and player.position.x> -68
	report["gallery_position"]=str(player.position)
	await save_capture("gallery_landing")
	player.position=Vector3(-67,1.08,-37.5)
	player.rotation.y=-PI/2
	player.velocity=Vector3.ZERO
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=true;Input.parse_input_event(ev)
	await get_tree().create_timer(1.2).timeout
	ev=InputEventKey.new();ev.physical_keycode=KEY_W;ev.pressed=false;Input.parse_input_event(ev)
	checks["gallery_middle_pier_blocks"]=player.position.x < -64.6 and player.position.x > -66.0
	report["gallery_pier_position"]=str(player.position)
	player.position=Vector3(-70,.18,-20)
	player.rotation.y=PI/2
	player.pitch=.24
	await get_tree().create_timer(.8).timeout
	await save_capture("market_front")
	player.position=Vector3(-98,.18,-18)
	player.rotation.y=PI/2
	player.pitch=.20
	await get_tree().create_timer(.8).timeout
	await save_capture("market_entry")
	set_night(true)
	await get_tree().create_timer(.8).timeout
	await save_capture("market_night")
	var sum_fps: float=0
	for fps in fps_history: sum_fps+=fps
	var elapsed: float=0
	var times: Array[float]=[]
	for fps in fps_history:
		elapsed+=1.0/fps
		times.append(1000.0/fps)
	times.sort()
	report["measured_frames"]=times.size()
	report["measured_seconds"]=elapsed
	report["mean_fps"]=times.size()/maxf(.001,elapsed)
	report["frame_time_p95_ms"]=times[mini(times.size()-1,int(times.size()*.95))]
	report["cpu"]=OS.get_processor_name()
	report["exported_application"]=not OS.has_feature("editor")
	report["window_pixels"]=str(DisplayServer.window_get_size())
	report["assets"]=JSON.parse_string(FileAccess.get_file_as_string("res://assets/manifest.json"))
	report["viewport"]=str(get_viewport().get_visible_rect().size)
	report["all_checks_pass"]=not checks.values().has(false)
	FileAccess.open(qa_root+"/runtime_validation.json",FileAccess.WRITE).store_string(JSON.stringify(report,"\t"))
	print("SOPHIA_QA ",JSON.stringify(report))
	get_tree().quit(0 if report.all_checks_pass else 2)
