from Duck_PA.teachers.classteacher import ClassTeacher

teacher1 = ClassTeacher(1, "William Thompson", ["Mathematics", "Computer science"], "Calm")
teacher2 = ClassTeacher(2, "Rachel Green", ["Physics", "Chemistry"], "Strict")
teacher3 = ClassTeacher(3, "Albert Taylor", ["Biology", "Geology"], "Friendly")
teacher4 = ClassTeacher(4, "Ira Abruzzo", ["English", "German", "Linguistics"], "Angry")

teachers = [teacher1, teacher2, teacher3, teacher4]

def get_teacher_by_id(teacher_id):
    """Get a teacher by their ID."""
    for teacher in teachers:
        if str(teacher.id) == str(teacher_id):
            return teacher
    return None