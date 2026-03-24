class DragManager:
    def __init__(self):
        self.drop_zones = []

    def register_zone(self, zone):
        if zone not in self.drop_zones:
            self.drop_zones.append(zone)

    def unregister_zone(self, zone):
        if zone in self.drop_zones:
            self.drop_zones.remove(zone)

    def get_hovered_zone(self, touch_pos):
        for zone in self.drop_zones:
            if zone.collide_point(*touch_pos):
                return zone
        return None
drag_manager = DragManager()