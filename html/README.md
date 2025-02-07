# Intelligent Birthday Butler

🎉 The Smart Birthday Manager is a powerful tool for managing and recording the birthdays of your friends and family. It supports both Gregorian and lunar calendars and provides thoughtful birthday reminders. Here is a detailed description of the project:

![Rendering 1](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/blob/main/html/rendering2.jpg)
![Rendering 2](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/blob/main/html/rendering1.jpg)

## Feature Overview

1. **Birthday Recording and Management**
   - Add, edit, and delete birthday information.
   - Support for both Gregorian and lunar calendar formats.
   - Automatically calculate age.

2. **Smart Reminders**
   - Check daily for birthdays and remind via notifications.
   - Support for browser notifications.

3. **Data Backup and Recovery**
   - Export birthday data as a JSON file.
   - Import birthday data from a JSON file.

4. **Theme Switching**
   - Support for light and dark modes.
   - Automatically switch themes based on the system or manually.

5. **Search and Sort**
   - Search for birthday records.
   - Sort by name, birth date, birthday type, and age.

6. **Animations and Interactions**
   - Modal, notification, and button animations.
   - Enhanced user interaction experience.

## Project Structure

- `index.html`: The main page file, containing HTML structure and some JavaScript logic.
- `styles.css`: The stylesheet file, defining the visual style and animation effects of the page.
- `scripts.js`: The main JavaScript file, containing the implementation of functions and interaction logic.

## Usage Instructions

### 1. Installation and Running

1. Clone or download this project.
2. Ensure your device is connected to the internet (some features require loading external libraries).
3. Open the `index.html` file to run it.

### 2. Adding a Birthday

1. Click the **➕ 添加生日** button on the page.
2. In the pop-up modal, enter the name and birthday information.
   - Select **阳历** or **农历**.
   - If you choose the lunar calendar, enter the year, month, and day.
3. Click the **✔️ 保存** button to complete the addition.

### 3. Editing a Birthday

1. Find the record you want to edit in the birthday list.
2. Click the **✏️ 编辑** button in the corresponding row.
3. After modifying the information, click the **✔️ 保存** button.

### 4. Deleting a Birthday

1. Find the record you want to delete in the birthday list.
2. Click the **🗑️ 删除** button in the corresponding row.
3. Click **✔️ 确定** in the confirmation modal.

### 5. Checking Birthdays

1. Click the **🔔 检查生日** button.
2. The system will check if there are any birthdays today and display reminders.

### 6. Exporting and Importing Data

- **Export Data**:
  1. Click the **📤 导出数据** button.
  2. The data will be saved as a `birthdays.json` file.
- **Import Data**:
  1. Click the **📥 导入数据** button.
  2. Select a JSON file (must be consistent with the export format).

### 7. Theme Switching

1. Click the theme switch button at the bottom right of the page.
2. The system will automatically switch between light and dark modes.

## Technology Stack

- **HTML**: Page structure.
- **CSS**: Style and animation.
- **JavaScript**: Function implementation and interaction logic.
- **Lunar-Calendar.js**: Conversion between lunar and Gregorian calendars.
- **SunCalc.js**: Automatic theme switching (based on geographical location and time).

## Notes

1. **Notification Permissions**:
   - When using the notification feature for the first time, please allow the notification permissions requested by the browser.
2. **Data Storage**:
   - Birthday data is stored in the browser's `localStorage` and will not be lost.
3. **Lunar Calendar Support**:
   - The lunar date range is from 1900 to 2100.

## Limitations

1. **Negative Age**:
   - You can choose a birth date after today.
2. **Notification Stacking**:
   - Notifications will stack together instead of expanding downward. This issue has not been resolved so far.

## Contributions and Feedback

If you find any issues or have suggestions for improvement, feel free to submit [issues](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/issues) or [pull requests](https://github.com/Jessssssseea/Intelligent-Birthday-Butler/pulls).

### Hope this birthday reminder program can help you better manage and remember the birthdays of your friends and family!
