class Settings():
    def __init__(self):
        self.screen_width = 900
        self.screen_height = 900
        self.bg_color = (243,222,187)
        self.initial_background = "image/kulami.jpg"
        self.hole_size = 50
        self.tile_edge_color = (150, 127, 103)
        self.font_color = (154, 202, 64)
        self.font = 'image/Phosphate-Solid.ttf'
        # 0 means robot first, 1 means player first
        self.robot_turn = 1
        # robot IQ means how deep tree search
        self.robot_IQ = 2
        self.trainset_address = "trainset"
