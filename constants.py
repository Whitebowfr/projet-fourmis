DECAY_RATE = 0.5
SPREAD_RATE: int = 10

NUMBER_OF_PHEROMONES: int = 2

SENSOR_OFFSET_DISTANCE: int = 15
SENSOR_SIZE: int = 5
SENSOR_ANGLE_RAD: float = 45 * 3.14 / 180
LOST_SPEED: float = 0.3
DETECTION_RANGE: int = 5

TURN_SPEED: float = 150 * 3.14/180
MOVE_SPEED: int = 150
RANDOM_FACT: int = 5

HOME_SIZE: int = 20
FOOD_SIZE: int = 20
FOOD_COUNT: int = 20

BG_BRIGHTNESS = 0.5

HIDE_MARKERS: bool = False

TRESHOLD: float = 0.1
BACK_TURN_FORCE: float = 0.3

colors = {"fourmis": "#FF0000",
          "food": "#00FF00",
          "maison": "#FFA500",
          "obstacles": "#646464",
          "pheromones": ["#FF0000", "#0000FF"]}

DEFAULT_PAINT_SIZE: int = 20

HOME_ZOOM_FACTOR: int = 1