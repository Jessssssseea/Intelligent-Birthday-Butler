# Intelligent Birthday Butler

## Introduction
The Birthday Reminder Program is a Python-based graphical user interface (GUI) application designed to help users record and manage contact birthdays and provide reminder functionality on their birthdays. Users can add, edit, and delete contacts, and sort the contact list based on different criteria.

![Rendering](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/blob/python-version/rendering.png)

## Features
1. **Contact Management**: Supports adding, editing, and deleting basic contact information, including name, birthday, and birthday type (lunar or Gregorian).
2. **Birthday Reminder**: Checks daily at a set time whether any contacts have birthdays and displays a reminder window to inform the user. Users can choose to no longer receive birthday reminders for a contact on that day.
3. **Sorting Functionality**: Allows sorting of the contact list in ascending or descending order by name, birthday, birthday type, and age.
4. **Date Selection**: Provides a calendar interface to facilitate the selection of birthday dates.

## Installation and Running
### Dependency Environment
This program requires a Python 3.x environment and depends on the following third-party libraries:
- `sxtwl`: For calculating lunar dates.
- `tkcalendar`: Provides calendar widgets for Tkinter to facilitate date selection.

### Installing Dependencies
You can install the required third-party libraries using the following command:
```bash
pip install -r requirements.txt
```

### Running the Program
After installing the dependencies, run the main program file directly:
```bash
python main.py
```

## Usage Instructions
1. ***Starting the Program***: After running the main program, a GUI window titled "生日提醒程序" will pop up.
2. ***Adding a Contact***: Click the "添加联系人" button and follow the prompts to enter the contact's name, select the birthday date, and choose the birthday type.
3. ***Editing a Contact***: Select the contact you want to edit from the contact list, then click the "编辑联系人" button to modify the relevant information.
4. ***Deleting a Contact***: Select the contact you want to delete and click the "删除联系人" button.
5. ***Checking Birthdays***: Click the "检查今天谁生日" button to manually check for contacts with birthdays today; the program will also automatically check for birthdays daily.
6. ***Sorting***: Click on the list headers "姓名" "生日" "类型" or "年龄" to sort the contact list based on the corresponding criteria.

## Code Structure
1. ***`BirthdayReminder` Class***: The core class of the program, responsible for initializing the interface, database operations, contact management, and birthday reminders.
2. ***Database Operations***: Uses the `sqlite3` library to create and manage the `birthday.db` database, which stores contact information.
3. ***Graphical Interface***: Creates a user interface based on the `tkinter` library, including components such as lists, buttons, and dialog boxes.
4. ***Date Handling***: Uses the `datetime` library and `sxtwl` library to handle dates and times, including birthday calculations and lunar date conversions.

## Limitations
1. ***Abnormal Lunar Date Display***
2. ***Potential Bugs in Auto-Start Function***

## Contributions and Feedback
If you find any issues or have suggestions for improvement, feel free to submit [issues](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/issues) or [pull requests](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/pulls).

### We hope this birthday reminder program can help you better manage and remember the birthdays of your friends and family!