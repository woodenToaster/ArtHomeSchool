import argparse
import datetime
import os
import sys
import time
import zipfile

days_in_month = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

main_link = ('For full context, see the description of my Art Home School Curriculum. '
             'https://litmusik.medium.com/art-home-school-introduction-f0e7027af017')

def get_next_n_days(n, month, day, year):
    result = []
    for _ in range(n):
        date_dir = "{}_{}_{}".format(month, day, year)
        result.append(date_dir)

        if day == days_in_month[month]:
            month += 1
            day = 1
        else:
            day += 1

        if month == 13:
            month = 1
            year += 1

    return result

def log_create_dir(dir_name):
    print("Creating directory '{}'".format(dir_name))

def init_unit(unit_dir, month, day):
    if args.day > days_in_month[args.month]:
        sys.exit("There are only {} days in month {}".format(days_in_month[args.month], args.month))

    assert(args.day)
    assert(args.month)

    log_create_dir(unit_dir)
    os.mkdir(unit_dir)
    year = int(time.strftime("%y"))
    weeks = ["Week{}".format(x + 1) for x in range(4)]
    for week in weeks:
        week_dir = os.path.join(unit_dir, week)
        log_create_dir(week_dir)
        os.mkdir(week_dir)

        num_days = 7
        days = get_next_n_days(num_days, month, day, year)

        starting_date = datetime.datetime.strptime("{}_{}_{}".format(month, day, year), "%m_%d_%y")
        end_date = (starting_date + datetime.timedelta(days=num_days)).date()

        day = end_date.day
        month = end_date.month
        year = end_date.year - 2000

        for date in days:
            date_path = os.path.join(week_dir, date)
            log_create_dir(date_path)
            os.mkdir(date_path)

def transfer_photos(unit_dir, week):
    assert(os.path.exists(unit_dir))

    week_dir = os.path.join(unit_dir, "Week{}".format(week))
    download_dir = 'C:/Users/Chris/Downloads'

    photos_fnames = [
        'Photos.zip',
        'Photos (1).zip',
        'Photos (2).zip',
        'Photos (3).zip',
        'Photos (4).zip',
        'Photos (5).zip',
        'Photos (6).zip',
    ]

    day_dirs = [x for x in os.listdir(week_dir) if os.path.isdir(os.path.join(week_dir, x))]
    for fname, i in zip(sorted(day_dirs, key=lambda date: datetime.datetime.strptime(date, '%m_%d_%y')),
                        range(len(day_dirs))):
        folder_path = os.path.join(week_dir, fname)
        zip_path = os.path.join(download_dir, photos_fnames[i])

        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                print("Extracting {} to {}".format(zip_path, folder_path))
                zip_ref.extractall(folder_path)
            print("Removing {}".format(zip_path))
            os.remove(zip_path)


def gen_plan_skeleton():
    print(main_link)
    print()
    print('Resources')
    print()
    print('Art Parent')
    print()
    print('Challenges')
    print()
    print('Inspiration')
    print()
    print('Exercises')

def gen_post_skeleton(month, day):
    print('For a description of this unit see my {} unit plan. ' + main_link)
    print()
    print('Retrospective')
    print()
    print('Log')
    print()
    print('Drawings and Critiques')
    print()

    for date in get_next_n_days(7, month, day, int(time.strftime('%y'))):
        dt = datetime.datetime.strptime(date, '%m_%d_%y')
        print(dt.strftime('%A, %b. %d'))
        print()

def main(args):
    base_dir = 'D:/drawing/work'

    if (args.unit):
        unit_dir = os.path.join(base_dir, args.unit)
        if (args.day and args.month):
            init_unit(unit_dir, args.month, args.day)
        elif (args.week):
            transfer_photos(unit_dir, args.week)
        else:
            sys.exit("Either a day or a week is required with a unit")
    elif args.plan:
        gen_plan_skeleton()
    elif args.post:
        assert(args.month)
        assert(args.day)
        gen_post_skeleton(args.month, args.day)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', help='The name of the unit')
    parser.add_argument('--month', type=int, help='The month number (January = 1)')
    parser.add_argument('--day', type=int, help='The start day of the month')
    parser.add_argument('--week', type=int, help='The week number to unzip photos for')
    parser.add_argument('--plan', action='store_true', help='Generate a skeleton for a unit plan blog post.')
    parser.add_argument('--post', action='store_true', help='Generate a skeleton for a weekly post.')
    args = parser.parse_args()

    main(args)
