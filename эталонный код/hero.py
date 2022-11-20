from control_keys import *

def startCameraAt(x, y, z):
    base.disableMouse()
    base.mouseInterfaceNode.setPos(-x, -y, -z)
    base.camera.reparentTo(render)
    base.enableMouse()

def check_dir(angle):
    ''' возвращает округленные изменения координат X, Y, 
    соответствующие перемещению в сторону угла angle.
    Координата Y уменьшается, если персонаж смотрит на угол 0,
    и увеличивается, если смотрит на угол 180.    
    Координата X увеличивается, если персонаж смотрит на угол 90,
    и уменьшается, если смотрит на угол 270.    
        угол 0 (от 0 до 20)      ->        Y - 1
        угол 45 (от 25 до 65)    -> X + 1, Y - 1
        угол 90 (от 70 до 110)   -> X + 1
        от 115 до 155            -> X + 1, Y + 1
        от 160 до 200            ->        Y + 1
        от 205 до 245            -> X - 1, Y + 1
        от 250 до 290            -> X - 1
        от 290 до 335            -> X - 1, Y - 1
        от 340                   ->        Y - 1  '''
    if angle >= 0 and angle <= 20:
        return (0, -1)
    elif angle <= 65:
        return (1, -1)
    elif angle <= 110:
        return (1, 0)
    elif angle <= 155:
        return (1, 1)
    elif angle <= 200:
        return (0, 1)
    elif angle <= 245:
        return (-1, 1)
    elif angle <= 290:
        return (-1, 0)
    elif angle <= 335:
        return (-1, -1)
    else:
        return (0, -1)

def next_cell(angle, x_from, y_from):
    dx, dy = check_dir(angle)
    return x_from + dx, y_from + dy

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True # режим прохождения сквозь всё
        self.btype = 0 # тип блока для строительства
        self.createHero(pos)
        self.cameraBind()
        self.accept_events()

    def createHero(self, pos):
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        # self.hero.setH(180) 
        self.hero.setPos(pos)
        self.hero.reparentTo(render)

    def cameraUp(self):
        pos = self.hero.getPos()
        startCameraAt(pos[0], pos[1], pos[2] + 3)
        self.cameraOn = False

    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        base.camera.setH(180)
        self.cameraOn = True

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)
        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_build, self.build)
        base.accept(key_btype_1, self.setBuild, [1])
        base.accept(key_btype_2, self.setBuild, [2])
        base.accept(key_btype_3, self.setBuild, [3])
        base.accept(key_destroy, self.destroy)
    
    def look_at(self, angle=None):
        ''' возвращает координаты, в которые переместится персонаж, стоящий в точке (x, y),
        если он делает шаг в направлении angle'''
        if angle is None:
            angle = self.hero.getH() % 360

        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        x_to, y_to = next_cell(angle, x_from, y_from)
        return x_to, y_to, z_from

    def just_move(self, angle):
        '''перемещается в нужные координаты в любом случае'''
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        '''перемещается, если может'''
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            # перед нами свободно. Возможно, надо упасть вниз:
            x, y, z = pos
            pos = self.land.findHighestEmpty(x, y)
            self.hero.setPos(pos)
        else:
            # перед нами занято. Если получится, заберёмся на этот блок:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
                # не получится забраться - стоим на месте

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
    
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() - 90) % 360
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def setBuild(self, type):
        self.btype = type

    def build(self):
        pos = self.look_at()
        if self.mode:
            self.land.addBlock(pos, type=self.btype)
        else:
            self.land.buildBlock(pos, type=self.btype)

    def destroy(self):
        pos = self.look_at()
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)
