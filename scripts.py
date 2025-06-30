import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

import random
from datacenter.models import Schoolkid
from datacenter.models import Subject
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Commendation 


def find_schoolkid(full_name):
    try:
        schoolkid = Schoolkid.objects.get(
            full_name=full_name,
            year_of_study='6',
            group_letter="А"
        )
        if schoolkid is None:
            print(f"Ученика с именем '{full_name}' не найдено.")
        return schoolkid
    except Schoolkid.DoesNotExist:
        print(f"Ученика с именем '{full_name}' не найдено.")
        return None
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем '{full_name}'.")
        return None


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    deleted_count, _ = chastisements.delete()


def create_commendation(schoolkid, subject, commendation_texts):
    lesson = Lesson.objects.filter(
        subject__in=subject,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
    ).last()
    if lesson:
        commendation_text = random.choice(commendation_texts)
        commendation = Commendation.objects.create(
            text=commendation_text,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
        commendation.save()
    else:
        print('Урок не найден.')


def main():
    full_name = "Фролов Иван Григорьевич"
    commendation_texts = [
        'Великолепно!',
        'Ты меня приятно удивил!',
        'Талантливо!'
    ]
    schoolkid = find_schoolkid(full_name)
    if schoolkid:
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        subject = Subject.objects.filter(title='Музыка', year_of_study=6)
        create_commendation(schoolkid, subject, commendation_texts)


if __name__ == '__main__':
    main()
