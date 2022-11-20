def new_sample():
    """Cоздаёт строительный блок для сооружения мира"""
    # загружаем модель, текстуру, устанавливаем текстуру:
    block = loader.loadModel('block')
    block.setTexture(loader.loadTexture('block.png'))

    return block

def getColor(z):
    colors = [
        (0.2, 0.2, 0.35, 1),
        (0.2, 0.5, 0.2, 1),
        (0.0, 0.6, 0.0, 1),
        (0.5, 0.3, 0.0, 1)
    ]
    if z < len(colors):
        return colors[z]
    else:
        return colors[len(colors) - 1]

class Blocks():
    """Класс для работы со строительными блоками, из которых состоит игровое поле (карта)
    
    Хранит: образец, по которому создаются блоки,
            узел, потомками которого будут все блоки
            выделенный узел;
    Умеет: создавать, удалять, выделять блок.
    """

    def __init__(self):
        self.sample = new_sample() # создали образец
        self.start_new()

    def start_new(self):
        """создаёт основу для новой карты""" 
        self.land = render.attachNewNode("Land") # узел, к которому привязаны все блоки карты
    
    def addBlock(self, position, color=None, land=True):
        """добавляет блок указанного цвета в указанное место"""
        # если цвет не задан
        if color is None:
            color = getColor(position[2])

        # создаём блок по образцу и устанавливаем, как просили:
        block = self.sample.copyTo(self.land)
        block.setPos(position)
        block.setColor(color)
        return block

    def addCol(self, x, y, z):
        for z0 in range(z+1):
            block = self.addBlock((x, y, z0))
        block.setTag("at", str(x) + str(y))
        block.setTag("height", str(z))

    def clear(self):
        """обнуляет карту"""
        self.land.removeNode()
        self.start_new()

    def getRoot(self):
        """возвращает корневой узел всех блоков карты"""
        return self.land

    def getAll(self):
        """возвращает коллекцию NodePath для всех существующих в карте мира блоков""" 
        return self.land.getChildren()

