// 自动主题切换功能
function updateThemeBySun() {
    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        const now = new Date();
        const times = SunCalc.getTimes(now, latitude, longitude);

        const isNight = now > times.sunset || now < times.sunrise;
        const theme = isNight ? 'dark' : 'light';

        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('autoTheme', 'true');
        localStorage.setItem('theme', theme);
    }, () => {
        console.log('无法获取位置信息，使用手动主题设置');
    });
}

// 每小时检查一次
updateThemeBySun();
setInterval(updateThemeBySun, 3600000);

// 初始化时检查自动主题
function applyTheme() {
    const autoTheme = localStorage.getItem('autoTheme') === 'true';
    if (!autoTheme) {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
    }
}

// 修改主题切换功能
const themeButton = document.getElementById('themeButton');
themeButton.addEventListener('change', (e) => {
    const isDark = e.detail === 'dark';
    localStorage.setItem('autoTheme', 'false');
    document.body.setAttribute('data-theme', isDark ? 'dark' : '');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// 修改应用主题方法
function applyTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme === 'dark' ? 'dark' : '');
    themeButton.setAttribute('value', savedTheme);
}

// 数据存储
let contacts = JSON.parse(localStorage.getItem('birthdayContacts')) || [];
let currentEditIndex = -1;
let sortConfig = { key: null, ascending: true };
let deleteIndex = -1;

// 初始化
function init() {
    applyTheme();
    renderTable();
    requestNotificationPermission();
    checkBirthdaysOnLoad();
}

// 页面加载时检查生日
function checkBirthdaysOnLoad() {
    const lastCheck = localStorage.getItem('lastBirthdayCheck');
    const today = new Date().toDateString();

    if (!lastCheck || lastCheck !== today) {
        checkBirthdays();
        localStorage.setItem('lastBirthdayCheck', today);
    }
}

// 请求通知权限
function requestNotificationPermission() {
    if (Notification.permission !== 'granted') {
        Notification.requestPermission();
    }
}

// 渲染表格
function renderTable(filteredContacts = contacts) {
    const tbody = document.getElementById('contactsBody');
    tbody.innerHTML = '';

    filteredContacts.forEach((contact, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${contact.name}</td>
            <td>${contact.displayDate}</td>
            <td>${contact.type}</td>
            <td>${calculateAge(contact.birthday)}</td>
            <td>
                <button onclick="editContact(${index})">✏️ 编辑</button>
                <button class="secondary" onclick="openDeleteConfirmModal(${index})">🗑️ 删除</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 计算年龄
function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    return age;
}

// 打开添加模态框
function openAddModal() {
    currentEditIndex = -1;
    resetForm();
    document.getElementById('modalTitle').textContent = '添加生日';
    document.getElementById('editModal').style.display = 'flex';
}

// 编辑联系人
function editContact(index) {
    currentEditIndex = index;
    const contact = contacts[index];

    document.getElementById('editName').value = contact.name;
    document.getElementById('modalTitle').textContent = '编辑生日';

    if (contact.type === '农历') {
        document.getElementById('lunarType').checked = true;
        document.getElementById('lunarYear').value = contact.lunarDate.year;
        document.getElementById('lunarMonth').value = contact.lunarDate.month;
        document.getElementById('lunarDay').value = contact.lunarDate.day;
    } else {
        document.getElementById('solarType').checked = true;
        document.getElementById('solarDate').value = contact.birthday;
    }

    toggleCalendarType();
    document.getElementById('editModal').style.display = 'flex';
}

// 切换日历类型
function toggleCalendarType() {
    const isLunar = document.getElementById('lunarType').checked;
    document.querySelector('.solar-fields').style.display = isLunar ? 'none' : 'block';
    document.querySelector('.lunar-fields').style.display = isLunar ? 'grid' : 'none';
}

// 保存联系人
function saveContact() {
    const contact = {
        name: document.getElementById('editName').value.trim(),
        type: document.querySelector('input[name="calendarType"]:checked').value
    };

    if (!contact.name) {
        showNotification('请输入姓名');
        return;
    }

    if (contact.type === '农历') {
        contact.lunarDate = {
            year: parseInt(document.getElementById('lunarYear').value),
            month: parseInt(document.getElementById('lunarMonth').value),
            day: parseInt(document.getElementById('lunarDay').value)
        };

        if (!validateLunarDate(contact.lunarDate)) {
            showNotification('请输入有效的农历日期');
            return;
        }

        const solarDate = LunarCalendar.lunarToSolar(
            contact.lunarDate.year,
            contact.lunarDate.month,
            contact.lunarDate.day
        );
        contact.birthday = `${solarDate.year}-${String(solarDate.month).padStart(2, '0')}-${String(solarDate.day).padStart(2, '0')}`;
        contact.displayDate = `${contact.lunarDate.year}年${contact.lunarDate.month}月${contact.lunarDate.day}日（农历）`;
    } else {
        const dateInput = document.getElementById('solarDate').value;
        if (!dateInput) {
            showNotification('请选择日期');
            return;
        }
        contact.birthday = dateInput;
        contact.displayDate = new Date(dateInput).toLocaleDateString('zh-CN');
    }

    if (currentEditIndex === -1) {
        contacts.push(contact);
    } else {
        contacts[currentEditIndex] = contact;
    }

    localStorage.setItem('birthdayContacts', JSON.stringify(contacts));
    renderTable();
    closeModal();
    showNotification('保存成功！', 'success');
}

// 验证农历日期
function validateLunarDate(date) {
    return date.year >= 1900 && date.year <= 2100 &&
        date.month >= 1 && date.month <= 12 &&
        date.day >= 1 && date.day <= 30;
}

// 打开删除确认模态框
function openDeleteConfirmModal(index) {
    deleteIndex = index;
    document.getElementById('deleteConfirmModal').style.display = 'flex';
}

// 确认删除
function confirmDelete() {
    if (deleteIndex !== -1) {
        contacts.splice(deleteIndex, 1);
        localStorage.setItem('birthdayContacts', JSON.stringify(contacts));
        renderTable();
        showNotification('已删除', 'warning');
        closeDeleteConfirmModal();
    }
}

// 检查生日
function checkBirthdays() {
    const today = new Date();
    const currentMonth = today.getMonth() + 1;
    const currentDay = today.getDate();
    let reminders = [];

    contacts.forEach(contact => {
        const birthDate = new Date(contact.birthday);
        const birthMonth = birthDate.getMonth() + 1;
        const birthDay = birthDate.getDate();

        if (contact.type === '农历') {
            const currentYear = today.getFullYear();
            const solarDate = LunarCalendar.lunarToSolar(
                currentYear,
                contact.lunarDate.month,
                contact.lunarDate.day
            );
            if (solarDate.month === currentMonth && solarDate.day === currentDay) {
                reminders.push(contact);
            }
        } else if (birthMonth === currentMonth && birthDay === currentDay) {
            reminders.push(contact);
        }
    });

    if (reminders.length > 0) {
        const message = reminders.map(c => `🎉 今天是 ${c.name} 的${c.type}生日！`).join('\n');
        showNotification(message, 'success', 5000);
        if (Notification.permission === 'granted') {
            new Notification('生日提醒', { body: message });
        }
    } else {
        showNotification('今天没有人生日！', 'info');
        new Notification('检查结果：今天没有人生日！');
    }
}

function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // 获取或创建通知容器
    const notificationsContainer = document.getElementById('notificationsContainer') || createNotificationsContainer();

    // 添加通知到容器中
    notificationsContainer.appendChild(notification);

    // 显示动画
    setTimeout(() => notification.classList.add('visible'), 10);

    // 设置移除通知的逻辑
    setTimeout(() => {
        notification.classList.remove('visible');
        notification.addEventListener('transitionend', () => {
            notification.remove(); // 在动画结束后移除通知
        }, {once: true});
    }, duration);
}

// 创建通知容器函数
function createNotificationsContainer() {
    const container = document.createElement('div');
    container.id = 'notificationsContainer';
    container.style.display = 'flex';
    container.style.flexDirection = 'column'; // 确保新通知位于下方
    container.style.gap = '10px';
    container.style.position = 'fixed';
    container.style.top = '1rem';
    container.style.right = '1rem';
    container.style.width = '200px';
    document.body.appendChild(container);
    return container;
}

// 修改关闭模态框函数
function closeModal() {
    const modal = document.getElementById('editModal');
    const modalContent = modal.querySelector('.modal-content');
    modalContent.classList.add('closing');

    setTimeout(() => {
        modal.style.display = 'none';
        modalContent.classList.remove('closing');
    }, 200);
}

// 修改关闭删除确认框函数
function closeDeleteConfirmModal() {
    const modal = document.getElementById('deleteConfirmModal');
    const modalContent = modal.querySelector('.modal-content');
    modalContent.classList.add('closing');

    setTimeout(() => {
        modal.style.display = 'none';
        modalContent.classList.remove('closing');
    }, 200);
}

// 重置表单
function resetForm() {
    document.getElementById('editName').value = '';
    document.getElementById('solarDate').value = '';
    document.getElementById('lunarYear').value = '';
    document.getElementById('lunarMonth').value = '';
    document.getElementById('lunarDay').value = '';
    document.getElementById('solarType').checked = true;
    toggleCalendarType();
}

// 搜索过滤
function filterContacts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = contacts.filter(c =>
        c.name.toLowerCase().includes(searchTerm) ||
        c.displayDate.toLowerCase().includes(searchTerm)
    );
    renderTable(filtered);
}

// 表格排序
function sortBy(key) {
    if (sortConfig.key === key) {
        sortConfig.ascending = !sortConfig.ascending;
    } else {
        sortConfig = { key, ascending: true };
    }

    contacts.sort((a, b) => {
        let compareValue = 0;

        switch (key) {
            case 'name':
                compareValue = a.name.localeCompare(b.name);
                break;
            case 'birthday':
                compareValue = new Date(a.birthday) - new Date(b.birthday);
                break;
            case 'type':
                compareValue = a.type.localeCompare(b.type);
                break;
            case 'age':
                compareValue = calculateAge(a.birthday) - calculateAge(b.birthday);
                break;
        }

        return sortConfig.ascending ? compareValue : -compareValue;
    });

    renderTable();
}

// 数据备份
function exportData() {
    const data = JSON.stringify(contacts, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'birthdays.json';
    a.click();
    URL.revokeObjectURL(url);
    showNotification('数据已导出到 birthdays.json 文件', 'success');
}

// 数据恢复
function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    const data = JSON.parse(event.target.result);
                    contacts = data; // 更新联系人数据
                    localStorage.setItem('birthdayContacts', JSON.stringify(contacts)); // 保存到本地存储
                    renderTable(); // 重新渲染表格
                    showNotification('数据已成功导入', 'success');
                } catch (error) {
                    console.error('导入失败：', error);
                    showNotification('导入失败，请确保文件格式为“.json”', 'error');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

// 初始化程序
init();

// 自定义主题按钮组件
(() => {
    const func = (root, initTheme, changeTheme) => {
        const $ = (s) => {
            let dom = root.querySelectorAll(s);
            return dom.length == 1 ? dom[0] : dom;
        };
        let mainButton = $(".main-button");
        let daytimeBackground = $(".daytime-background");
        let cloud = $(".cloud");
        let cloudList = $(".cloud-son");
        let cloudLight = $(".cloud-light");
        let components = $(".components");
        let moon = $(".moon");
        let stars = $(".stars");
        let star = $(".star");
        let isMoved = false;
        let isClicked = false;
        window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
            toggleThemeBasedOnSystem();
        });
        const toggleThemeBasedOnSystem = () => {
            if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
                if (!isMoved) {
                    components.onclick();
                }
            } else {
                if (isMoved) {
                    components.onclick();
                }
            }
        };
        components.onclick = () => {
            if (isMoved) {
                mainButton.style.transform = "translateX(0)";
                mainButton.style.backgroundColor = "rgba(255, 195, 35,1)";

                mainButton.style.boxShadow =
                    "3em 3em 5em rgba(0, 0, 0, 0.5), inset  -3em -5em 3em -3em rgba(0, 0, 0, 0.5), inset  4em 5em 2em -2em rgba(255, 230, 80,1)";

                daytimeBackground[0].style.transform = "translateX(0)";
                daytimeBackground[1].style.transform = "translateX(0)";
                daytimeBackground[2].style.transform = "translateX(0)";
                cloud.style.transform = "translateY(10em)";
                cloudLight.style.transform = "translateY(10em)";
                components.style.backgroundColor = "rgba(70, 133, 192,1)";

                moon[0].style.opacity = "0";
                moon[1].style.opacity = "0";
                moon[2].style.opacity = "0";

                stars.style.transform = "translateY(-125em)";
                stars.style.opacity = "0";

                changeTheme("light");
            } else {
                mainButton.style.transform = "translateX(110em)";
                mainButton.style.backgroundColor = "rgba(195, 200,210,1)";

                mainButton.style.boxShadow =
                    "3em 3em 5em rgba(0, 0, 0, 0.5), inset  -3em -5em 3em -3em rgba(0, 0, 0, 0.5), inset  4em 5em 2em -2em rgba(255, 255, 210,1)";

                daytimeBackground[0].style.transform = "translateX(110em)";
                daytimeBackground[1].style.transform = "translateX(80em)";
                daytimeBackground[2].style.transform = "translateX(50em)";
                cloud.style.transform = "translateY(80em)";
                cloudLight.style.transform = "translateY(80em)";
                components.style.backgroundColor = "rgba(25,30,50,1)";

                moon[0].style.opacity = "1";
                moon[1].style.opacity = "1";
                moon[2].style.opacity = "1";

                stars.style.transform = "translateY(-62.5em)";
                stars.style.opacity = "1";

                changeTheme("dark");
            }

            isClicked = true;

            setTimeout(function () {
                isClicked = false;
            }, 500);
            isMoved = !isMoved;
        };

        mainButton.addEventListener("mousemove", function () {
            if (isClicked) return;

            if (isMoved) {
                mainButton.style.transform = "translateX(100em)";
                daytimeBackground[0].style.transform = "translateX(100em)";
                daytimeBackground[1].style.transform = "translateX(73em)";
                daytimeBackground[2].style.transform = "translateX(46em)";

                star[0].style.top = "10em";
                star[0].style.left = "36em";
                star[1].style.top = "40em";
                star[1].style.left = "87em";
                star[2].style.top = "26em";
                star[2].style.left = "16em";
                star[3].style.top = "38em";
                star[3].style.left = "63em";
                star[4].style.top = "20.5em";
                star[4].style.left = "72em";
                star[5].style.top = "51.5em";
                star[5].style.left = "35em";
            } else {
                mainButton.style.transform = "translateX(10em)";
                daytimeBackground[0].style.transform = "translateX(10em)";
                daytimeBackground[1].style.transform = "translateX(7em)";
                daytimeBackground[2].style.transform = "translateX(4em)";

                cloudList[0].style.right = "-24em";
                cloudList[0].style.bottom = "10em";
                cloudList[1].style.right = "-12em";
                cloudList[1].style.bottom = "-27em";
                cloudList[2].style.right = "17em";
                cloudList[2].style.bottom = "-43em";
                cloudList[3].style.right = "46em";
                cloudList[3].style.bottom = "-39em";
                cloudList[4].style.right = "70em";
                cloudList[4].style.bottom = "-65em";
                cloudList[5].style.right = "109em";
                cloudList[5].style.bottom = "-54em";
                cloudList[6].style.right = "-23em";
                cloudList[6].style.bottom = "10em";
                cloudList[7].style.right = "-11em";
                cloudList[7].style.bottom = "-26em";
                cloudList[8].style.right = "18em";
                cloudList[8].style.bottom = "-42em";
                cloudList[9].style.right = "47em";
                cloudList[9].style.bottom = "-38em";
                cloudList[10].style.right = "74em";
                cloudList[10].style.bottom = "-64em";
                cloudList[11].style.right = "110em";
                cloudList[11].style.bottom = "-55em";
            }
        });

        mainButton.addEventListener("mouseout", function () {
            if (isClicked) {
                return;
            }
            if (isMoved) {
                mainButton.style.transform = "translateX(110em)";
                daytimeBackground[0].style.transform = "translateX(110em)";
                daytimeBackground[1].style.transform = "translateX(80em)";
                daytimeBackground[2].style.transform = "translateX(50em)";

                star[0].style.top = "11em";
                star[0].style.left = "39em";
                star[1].style.top = "39em";
                star[1].style.left = "91em";
                star[2].style.top = "26em";
                star[2].style.left = "19em";
                star[3].style.top = "37em";
                star[3].style.left = "66em";
                star[4].style.top = "21em";
                star[4].style.left = "75em";
                star[5].style.top = "51em";
                star[5].style.left = "38em";
            } else {
                mainButton.style.transform = "translateX(0em)";
                daytimeBackground[0].style.transform = "translateX(0em)";
                daytimeBackground[1].style.transform = "translateX(0em)";
                daytimeBackground[2].style.transform = "translateX(0em)";

                cloudList[0].style.right = "-20em";
                cloudList[0].style.bottom = "10em";
                cloudList[1].style.right = "-10em";
                cloudList[1].style.bottom = "-25em";
                cloudList[2].style.right = "20em";
                cloudList[2].style.bottom = "-40em";
                cloudList[3].style.right = "50em";
                cloudList[3].style.bottom = "-35em";
                cloudList[4].style.right = "75em";
                cloudList[4].style.bottom = "-60em";
                cloudList[5].style.right = "110em";
                cloudList[5].style.bottom = "-50em";
                cloudList[6].style.right = "-20em";
                cloudList[6].style.bottom = "10em";
                cloudList[7].style.right = "-10em";
                cloudList[7].style.bottom = "-25em";
                cloudList[8].style.right = "20em";
                cloudList[8].style.bottom = "-40em";
                cloudList[9].style.right = "50em";
                cloudList[9].style.bottom = "-35em";
                cloudList[10].style.right = "75em";
                cloudList[10].style.bottom = "-60em";
                cloudList[11].style.right = "110em";
                cloudList[11].style.bottom = "-50em";
            }
        });

        const getRandomDirection = () => {
            const directions = ["2em", "-2em"];
            return directions[Math.floor(Math.random() * directions.length)];
        };

        const moveElementRandomly = (element) => {
            const randomDirectionX = getRandomDirection();
            const randomDirectionY = getRandomDirection();
            element.style.transform = `translate(${randomDirectionX}, ${randomDirectionY})`;
        };

        const cloudSons = root.querySelectorAll(".cloud-son");
        setInterval(() => {
            cloudSons.forEach(moveElementRandomly);
        }, 1000);

        if (initTheme === "dark") {
            components.onclick();
        }
    };

    class ThemeButton extends HTMLElement {
        constructor() {
            super();
        }
        connectedCallback() {
            const initTheme = this.getAttribute("value") || "light";
            const size = +this.getAttribute("size") || 3;
            const shadow = this.attachShadow({ mode: "closed" });
            const container = document.createElement("div");
            container.setAttribute("class", "container");
            container.setAttribute("style", `font-size: ${(size / 3).toFixed(2)}px`);
            container.innerHTML =
                '<div class="components"><div class="main-button"><div class="moon"></div><div class="moon"></div><div class="moon"></div></div><div class="daytime-background"></div><div class="daytime-background"></div><div class="daytime-background"></div><div class="cloud"><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div></div><div class="cloud-light"><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div><div class="cloud-son"></div></div><div class="stars"><div class="star big"><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div></div><div class="star big"><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div></div><div class="star medium"><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div></div><div class="star medium"><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div></div><div class="star small"><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div></div><div class="star small"><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div><div class="star-son"></div></div></div></div>';
            const style = document.createElement("style");
            style.textContent =
                "* { margin: 0; padding: 0; transition: 0.7s; -webkit-tap-highlight-color:rgba(0,0,0,0); } .container { position: absolute;top: 50%;left: 50%;margin-top: -35em;margin-left: -90em;width: 180em; height: 70em; display: inline-block; vertical-align: bottom; transform: translate3d(0, 0, 0); } .components{ position:fixed; width: 180em; height: 70em; background-color: rgba(70, 133, 192,1); border-radius: 100em; box-shadow: inset 0 0 5em 3em rgba(0, 0, 0, 0.5); overflow: hidden; transition: 0.7s; transition-timing-function: cubic-bezier( 0,0.5, 1,1); cursor: pointer; } .main-button{ margin: 7.5em 0 0 7.5em; width: 55em; height:55em; background-color: rgba(255, 195, 35,1); border-radius: 50%; box-shadow:3em 3em 5em rgba(0, 0, 0, 0.5), inset -3em -5em 3em -3em rgba(0, 0, 0, 0.5), inset 4em 5em 2em -2em rgba(255, 230, 80,1); transition: 1.0s; transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00); } .moon{ position: absolute; background-color: rgba(150, 160, 180, 1); box-shadow:inset 0em 0em 1em 1em rgba(0, 0, 0, 0.3) ; border-radius: 50%; transition: 0.5s; opacity: 0; } .moon:nth-child(1){ top: 7.5em; left: 25em; width: 12.5em; height: 12.5em; } .moon:nth-child(2){ top: 20em; left: 7.5em; width: 20em; height: 20em; } .moon:nth-child(3){ top: 32.5em; left: 32.5em; width: 12.5em; height: 12.5em; } .daytime-background { position: absolute; border-radius: 50%; transition: 1.0s; transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00); } .daytime-background:nth-child(2){ top: -20em; left: -20em; width: 110em; height:110em; background-color: rgba(255, 255, 255,0.2); z-index: -2; } .daytime-background:nth-child(3){ top: -32.5em; left: -17.5em; width: 135em; height:135em; background-color: rgba(255, 255, 255,0.1); z-index: -3; } .daytime-background:nth-child(4){ top: -45em; left: -15em; width: 160em; height:160em; background-color: rgba(255, 255, 255,0.05); z-index: -4; } .cloud,.cloud-light{ transform: translateY(10em); transition: 1.0s; transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00); } .cloud-son{ position: absolute; background-color: #fff; border-radius: 50%; z-index: -1; transition: transform 6s,right 1s,bottom 1s; } .cloud-son:nth-child(6n+1){ right: -20em; bottom: 10em; width: 50em; height: 50em; } .cloud-son:nth-child(6n+2) { right: -10em; bottom: -25em; width: 60em; height: 60em; } .cloud-son:nth-child(6n+3) { right: 20em; bottom: -40em; width: 60em; height: 60em; } .cloud-son:nth-child(6n+4) { right: 50em; bottom: -35em; width: 60em; height: 60em; } .cloud-son:nth-child(6n+5) { right: 75em; bottom: -60em; width: 75em; height: 75em; } .cloud-son:nth-child(6n+6) { right: 110em; bottom: -50em; width: 60em; height: 60em; } .cloud{ z-index: -2; } .cloud-light{ position: absolute; right: 0em; bottom: 25em; opacity: 0.5; z-index: -3; /*transform: rotate(-5deg);*/ } .stars{ transform: translateY(-125em); z-index: -2; transition: 1.0s; transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00); } .big { --size: 7.5em; } .medium { --size: 5em; } .small { --size: 3em; } .star { position: absolute; width: calc(2*var(--size)); height: calc(2*var(--size)); } .star:nth-child(1){ top: 11em; left: 39em; animation-name: star; animation-duration: 3.5s; } .star:nth-child(2){ top: 39em; left: 91em; animation-name: star; animation-duration: 4.1s; } .star:nth-child(3){ top: 26em; left: 19em; animation-name: star; animation-duration: 4.9s; } .star:nth-child(4){ top: 37em; left: 66em; animation-name: star; animation-duration: 5.3s; } .star:nth-child(5){ top: 21em; left: 75em; animation-name: star; animation-duration: 3s; } .star:nth-child(6){ top: 51em; left: 38em; animation-name: star; animation-duration: 2.2s; } @keyframes star { 0%,20%{ transform: scale(0); } 20%,100% { transform: scale(1); } } .star-son{ float: left; } .star-son:nth-child(1) { --pos: left 0; } .star-son:nth-child(2) { --pos: right 0; } .star-son:nth-child(3) { --pos: 0 bottom; } .star-son:nth-child(4) { --pos: right bottom; } .star-son { width: var(--size); height: var(--size); background-image: radial-gradient(circle var(--size) at var(--pos), transparent var(--size), #fff); } .star{ transform: scale(1); transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00); transition: 1s; animation-iteration-count:infinite; animation-direction: alternate; animation-timing-function: linear; } .twinkle { transform: scale(0); }";
            const changeTheme = (detail) => {
                this.dispatchEvent(new CustomEvent("change", { detail }));
            };
            func(container, initTheme, changeTheme);
            shadow.appendChild(style);
            shadow.appendChild(container);
        }
    }

    customElements.define("theme-button", ThemeButton);
})();