class ClassTeacher:
    def __init__(self, id, name, specialization, attitude):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.attitude = attitude

    def to_dict(self):
        """
        Helper method to convert the ClassTeacher instance
        to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "attitude": self.attitude
        }