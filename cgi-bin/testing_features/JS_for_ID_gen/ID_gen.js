function generateSessionID() {
        let interm = '';
        const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        const length = 15; // Длина уникального идентификатора сессии

        const currentTime = new Date().getTime().toString(); // Получаем текущее время в миллисекундах

        for (let i = 0; i < length; i++) {
                const randomChar = characters.charAt(Math.floor(Math.random() * charactersLength));
                interm += randomChar;
        }

        result = currentTime + interm; // Добавляем текущее время к идентификатору сессии

        return result;
        }

const sessionID = generateSessionID();
let sessionIDStorage = window.sessionStorage;
sessionIDStorage.setItem('sessionID', sessionID);

function initCont() {
        const xhttp = new XMLHttpRequest();
        const url = 'cgi-bin/init_cont.py';
        const progr_lang = document.getElementById('lang_menu').value;
        const fileName = document.getElementById('file_name').value;
        const IDline = new FormData();
        IDline.append('sessionID', sessionID);
        IDline.append('progr_lang', progr_lang);
        IDline.append('file_name', fileName);

        xhttp.onreadystatechange = function() {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
                }
                };

                xhttp.open('POST', url, true);
                xhttp.send(IDline);
        }
