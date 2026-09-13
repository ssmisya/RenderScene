extends CharacterBody3D

var camera: Camera3D
var weapon: Node3D
var flash: OmniLight3D
var torch: SpotLight3D
var pitch: float = -0.10
var walking_time: float = 0.0
var step_time: float = 0.0
var recoil: float = 0.0
var cooldown: float = 0.0
var reload_time: float = 0.0
var ammo: int = 30
var shots_fired: int = 0
var is_aiming: bool = false
var gun_visible: bool = true
var enabled: bool = false
var main: Node3D
var shot_sound: AudioStreamPlayer
var foot_sound: AudioStreamPlayer
var reload_sound: AudioStreamPlayer
var step_assists: int = 0

func _ready() -> void:
	main = get_parent()
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 0.38
	floor_max_angle = deg_to_rad(48.0)
	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.30
	capsule.height = 1.78
	shape.shape = capsule
	shape.position.y = 0.91
	add_child(shape)
	camera = Camera3D.new()
	camera.position.y = 1.70
	camera.near = 0.04
	camera.far = 650.0
	camera.fov = 76.0
	add_child(camera)
	camera.current = true
	weapon = Node3D.new()
	camera.add_child(weapon)
	build_weapon()
	torch = SpotLight3D.new()
	torch.position = Vector3(0.15, -0.10, -0.25)
	torch.light_color = Color(1.0, 0.93, 0.80)
	torch.light_energy = 5.0
	torch.spot_range = 28.0
	torch.spot_angle = 26.0
	torch.shadow_enabled = true
	torch.visible = false
	camera.add_child(torch)
	shot_sound = make_sound("res://audio/shot.wav", -12)
	foot_sound = make_sound("res://audio/step.wav", -19)
	reload_sound = make_sound("res://audio/reload.wav", -12)
	reset_position()

func make_sound(path: String, volume: float) -> AudioStreamPlayer:
	var a := AudioStreamPlayer.new()
	a.stream = load(path)
	a.volume_db = volume
	add_child(a)
	return a

func reset_position() -> void:
	position = Vector3(-55, 0.18, 21)
	rotation.y = -1.18
	pitch = 0.12
	velocity = Vector3.ZERO

func material(color: Color, metallic: float = 0.0, rough: float = 0.6) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.metallic = metallic
	m.roughness = rough
	return m

func piece(size: Vector3, at: Vector3, mat: Material) -> MeshInstance3D:
	var mesh := BoxMesh.new()
	mesh.size = size
	var ob := MeshInstance3D.new()
	ob.mesh = mesh
	ob.material_override = mat
	ob.position = at
	ob.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	weapon.add_child(ob)
	return ob

func tube(radius: float, length: float, at: Vector3, mat: Material) -> MeshInstance3D:
	var mesh := CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius
	mesh.height = length
	mesh.radial_segments = 24
	var ob := MeshInstance3D.new()
	ob.mesh = mesh
	ob.material_override = mat
	ob.position = at
	ob.rotation.x = PI / 2
	ob.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	weapon.add_child(ob)
	return ob

func limb(a: Vector3, b: Vector3, radius: float, mat: Material) -> void:
	var mesh := CapsuleMesh.new()
	mesh.radius = radius
	mesh.height = a.distance_to(b) + radius * 2
	var ob := MeshInstance3D.new()
	ob.mesh = mesh
	ob.material_override = mat
	weapon.add_child(ob)
	ob.position = (a+b)/2
	ob.quaternion = Quaternion(Vector3.UP, (b-a).normalized())
	ob.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF

func build_weapon() -> void:
	# Original non-branded demonstration prop. No third-party weapon/IP assets.
	var steel := material(Color(0.085,0.10,0.115),0.72,0.36)
	var grip := material(Color(0.065,0.07,0.075),0.0,0.88)
	var tan := material(Color(0.27,0.29,0.20),0.08,0.78)
	var sleeve := material(Color(0.13,0.16,0.12),0.0,0.95)
	var gloves := material(Color(0.12,0.11,0.09),0.0,0.93)
	piece(Vector3(.085,.115,.30), Vector3(0,0,-.34),steel)
	piece(Vector3(.10,.10,.27), Vector3(0,-.015,-.59),tan)
	tube(.016,.23,Vector3(0,0,-.83),steel)
	tube(.025,.055,Vector3(0,0,-.96),grip)
	piece(Vector3(.071,.16,.095),Vector3(0,-.11,-.28),grip).rotation.x=-.22
	piece(Vector3(.06,.21,.115),Vector3(0,-.16,-.41),steel).rotation.x=.13
	piece(Vector3(.085,.095,.20),Vector3(0,-.01,-.105),tan)
	piece(Vector3(.095,.14,.03),Vector3(0,-.035,-.01),grip)
	for i in range(12):
		piece(Vector3(.105,.017,.008),Vector3(0,.058,-.72+i*.037),steel)
	for side in [-1.0,1.0]:
		for i in range(5):
			piece(Vector3(.006,.035,.029),Vector3(side*.052,-.014,-.69+i*.045),grip)
	piece(Vector3(.06,.017,.07),Vector3(0,.085,-.37),steel)
	for side in [-1.0,1.0]:
		piece(Vector3(.009,.048,.012),Vector3(side*.027,.108,-.37),steel)
	piece(Vector3(.06,.009,.012),Vector3(0,.132,-.37),steel)
	piece(Vector3(.008,.05,.009),Vector3(0,.088,-.70),steel)
	piece(Vector3(.006,.039,.095),Vector3(.045,-.004,-.34),grip)
	for z in [-.42,-.28]:
		tube(.009,.009,Vector3(.046,0,z),grip).rotation = Vector3(0,0,PI/2)
	limb(Vector3(.22,-.38,.15),Vector3(.09,-.17,-.24),.050,sleeve)
	limb(Vector3(.09,-.17,-.24),Vector3(.01,-.085,-.27),.043,gloves)
	limb(Vector3(-.28,-.38,.08),Vector3(-.11,-.18,-.53),.05,sleeve)
	limb(Vector3(-.11,-.18,-.53),Vector3(-.028,-.064,-.60),.043,gloves)
	for i in range(4):
		limb(Vector3(-.045,-.052-i*.009,-.59+i*.013),Vector3(.015,-.069-i*.007,-.59+i*.013),.009,gloves)
	flash = OmniLight3D.new()
	flash.position = Vector3(0,0,-1.0)
	flash.light_color = Color(1,0.62,0.18)
	flash.light_energy = 0.0
	flash.omni_range = 5
	weapon.add_child(flash)

func _unhandled_input(event: InputEvent) -> void:
	if not enabled: return
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotation.y -= event.relative.x * .002
		pitch = clampf(pitch-event.relative.y*.002,-1.42,1.42)
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_R: reload_gun()
			KEY_F: torch.visible = not torch.visible
			KEY_G: gun_visible = not gun_visible

func reload_gun() -> void:
	if reload_time <= 0 and ammo < 30:
		reload_time = 1.65
		reload_sound.play()

func fire() -> void:
	if cooldown > 0 or reload_time > 0 or not gun_visible or ammo <= 0: return
	ammo -= 1
	shots_fired += 1
	cooldown = .14
	recoil = .085
	flash.light_energy = 3.5
	shot_sound.pitch_scale = randf_range(.94,1.05)
	shot_sound.play()
	var start := camera.global_position
	var end := start-camera.global_basis.z*250.0
	var query := PhysicsRayQueryParameters3D.create(start,end,1)
	query.exclude = [get_rid()]
	var hit := get_world_3d().direct_space_state.intersect_ray(query)
	if not hit.is_empty(): main.impact(hit.position,hit.normal)

func _physics_process(delta: float) -> void:
	cooldown = maxf(0,cooldown-delta)
	recoil = move_toward(recoil,0,delta*.65)
	flash.light_energy = move_toward(flash.light_energy,0,delta*60)
	if reload_time>0:
		reload_time -= delta
		if reload_time<=0: ammo=30
	camera.rotation.x = pitch+recoil*.3
	if not enabled: return
	is_aiming = Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) and gun_visible and reload_time<=0
	if not main.qa_mode and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT): fire()
	var axis := Vector2(float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),float(Input.is_physical_key_pressed(KEY_S))-float(Input.is_physical_key_pressed(KEY_W))).limit_length()
	var direction := global_basis*Vector3(axis.x,0,axis.y)
	var speed := 3.8
	if Input.is_physical_key_pressed(KEY_SHIFT): speed=6.2
	if is_aiming: speed=2.1
	velocity.x = move_toward(velocity.x,direction.x*speed,delta*24)
	velocity.z = move_toward(velocity.z,direction.z*speed,delta*24)
	if not is_on_floor(): velocity.y -= 19.0*delta
	elif Input.is_physical_key_pressed(KEY_SPACE): velocity.y=6.0
	else: velocity.y=-.1
	# Step only over a real obstruction with free headroom and a supporting surface.
	var motion := Vector3(velocity.x,0,velocity.z)*delta
	if is_on_floor() and motion.length()>.002 and test_move(global_transform,motion):
		var raised := global_transform
		raised.origin.y += .32
		if not test_move(global_transform,Vector3.UP*.32) and not test_move(raised,motion):
			var probe := PhysicsRayQueryParameters3D.create(raised.origin+motion.normalized()*.40+Vector3.UP*.05,raised.origin+motion.normalized()*.40-Vector3.UP*.36,1)
			var hit := get_world_3d().direct_space_state.intersect_ray(probe)
			if not hit.is_empty() and hit.normal.y>.7 and hit.position.y>position.y+.01:
				position.y = hit.position.y+.015
				step_assists += 1
	move_and_slide()
	if position.y < -8: reset_position()
	var moving := Vector2(velocity.x,velocity.z).length()>.4 and is_on_floor()
	if moving:
		walking_time += delta*speed*2.8
		step_time += delta
		if step_time > .49*3.8/speed:
			step_time=0
			foot_sound.pitch_scale=randf_range(.9,1.12)
			foot_sound.play()
	var bob := Vector3(sin(walking_time)*.007,abs(cos(walking_time))*.009,0) if moving else Vector3.ZERO
	var target := Vector3(.24,-.23,-.26)
	if is_aiming: target=Vector3(0,-.107,-.20)
	if reload_time>0: target+=Vector3(.04,-.16,.08)
	weapon.position=weapon.position.lerp(target+bob+Vector3(0,0,recoil),minf(1,delta*14))
	weapon.rotation.z=lerp_angle(weapon.rotation.z,-.35 if reload_time>0 else 0.0,delta*10)
	weapon.visible=gun_visible
	camera.fov=lerpf(camera.fov,53.0 if is_aiming else 76.0,minf(1,delta*10))
