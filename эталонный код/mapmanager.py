import pickle

class Mapmanager():
    """ Управление картой """
    def __init__(self):
        model = 'block' # модель кубика лежит в файле block.egg
        # используются следующие текстуры: 
        textures = [
            'block.png',
            'stone.png',
            'wood.png',
            'brick.png'
        ]
        self.createSamples(model, textures) # создаём строительные блоки             

        # блоки "земли" в зависимости от высоты будут следующих цветов:
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.0, 0.6, 0.0, 1),
            (0.5, 0.3, 0.0, 1)
        ]
        # создаём основной узел карты:
        self.startNew() 

    def startNew(self):
        """создаёт основу для новой карты""" 
        self.land = render.attachNewNode("Land") # узел, к которому привязаны все блоки карты
    
    def createSamples(self, model, textures):
        self.samples = list()
        for tname in textures:
            block = loader.loadModel(model)
            block.setTexture(loader.loadTexture(tname))
            self.samples.append(block)

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position, type=0):
        """добавляет блок указанного типа в указанное место"""
        # block = loader.loadModel(self.model)
        if type >= len(self.samples):
            # если тип неизвестен, считаем, что это земля
            type = 0
        # block.setTexture(self.textures[type])
        block = self.samples[type].copyTo(self.land)
        block.setPos(position)
        # если это земля, ставим автоматический цвет
        if type == 0:
            color = self.getColor(int(position[2]))
            block.setColor(color)
        # запомним тип, чтобы можно было сохранять созданное:
        block.setTag("type", str(type))
        # запомним координаты
        block.setTag("at", str(position))
        # ставим созданный блок на сцену
        block.reparentTo(self.land)

    def addCol(self, x, y, z):
        for z0 in range(z+1):
            block = self.addBlock((x, y, z0))

    def findBlocks(self, position):
        return self.land.findAllMatches("=at=" + str(position))

    def isEmpty(self, position):
        blocks = self.findBlocks(position)
        if blocks:
            return False
        return True

    def findHighestEmpty(self, x, y):
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos, type):
        """Ставим блок с учётом гравитации: """
        x, y, z = pos
        new = self.findHighestEmpty(x, y)
        if new[2] <= z + 1:
            self.addBlock(new, type)

    def delBlock(self, position):
        """удаляет блоки в указанной позиции """
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = position
        x, y, z = self.findHighestEmpty(x, y)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            if int(block.getTag("type")) > 0:
                block.removeNode()

    def clear(self):
        """обнуляет карту"""
        self.land.removeNode()
        self.startNew()

    def getRoot(self):
        """возвращает корневой узел всех блоков карты"""
        return self.land

    def getAll(self):
        """возвращает коллекцию NodePath для всех существующих в карте мира блоков""" 
        return self.land.getChildren()

    def planeLand(self, width=20, length=20):
        self.clear()
        z = 0
        for x in range(width):
            for y in range(length):
                pos = (x, y, z) 
                self.addBlock(pos)


    def loadLand(self, filename):
        """создаёт карту земли из текстового файла, возвращает её размеры"""
        self.clear()
        with open(filename) as f:
            y = 0
            firstline = True
            for s in f:
                if firstline:
                    maxY = int(s)
                    firstline = False
                else:
                    line = map(int, s.split())
                    x = 0
                    for z in line:
                        self.addCol(x, maxY-y, z)
                        x += 1
                    y += 1

        return x, maxY

    def saveMap(self, filename):
        """сохраняет все блоки, включая постройки, в бинарный файл"""
        blocks = self.getAll()
        # открываем бинарный файл на запись
        fout = open(filename, 'wb')

        # сохраняем в начало файла количество блоков
        pickle.dump(len(blocks), fout)

        # обходим все блоки
        for block in blocks:
            # сохраняем позицию
            x, y, z = block.getPos()
            pos = (int(x), int(y), int(z))
            pickle.dump(pos, fout)
            # сохраняем тип
            pickle.dump(int(block.getTag("type")), fout)

        # закрываем файл
        fout.close()

    def loadMap(self, filename):
        # удаляем все блоки
        self.clear()

        # открываем бинарный файл на чтение
        fin = open(filename, 'rb')

        # считываем количество блоков
        lenght = pickle.load(fin)

        for i in range(lenght):
            # считываем позицию
            pos = pickle.load(fin)
            # считываем тип
            type = pickle.load(fin)

            # создаём новый блок
            self.addBlock(pos, type)

        # закрываем файл
        fin.close()
