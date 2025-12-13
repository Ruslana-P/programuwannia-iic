document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');

    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;

    const chineseChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%^&*()";

    // Стовпці
    const fontSize = 16;
    const columns = canvas.width / fontSize;

    // Масив крапель (одна крапля на стовпець)
    let drops = [];
    for (let i = 0; i < columns; i++) {
        // Початкова позиція Y кожної краплі
        drops[i] = 1; 
    }

    // Головна функція малювання
    function draw() {
        // Злегка затінюємо старий вміст (ефект розмиття/затухання)
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Встановлюємо стиль тексту
        ctx.fillStyle = '#0F0'; // Яскраво-зелений
        ctx.font = fontSize + 'px arial';

        // Проходимося по кожній краплі
        for (let i = 0; i < drops.length; i++) {
            // Вибираємо випадковий символ
            const text = chineseChars[Math.floor(Math.random() * chineseChars.length)];

            // Малюємо символ
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            // Якщо крапля досягла нижнього краю, або випадково скидаємо її
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            // Збільшуємо позицію Y, щоб символ рухався вниз
            drops[i]++;
        }
    }

    // Цикл анімації
    setInterval(draw, 33); // Частота оновлення (приблизно 30 кадрів на секунду)

    // Обробка зміни розміру вікна
    window.addEventListener('resize', () => {
        canvas.height = window.innerHeight;
        canvas.width = window.innerWidth;
        const newColumns = canvas.width / fontSize;
        drops = Array(newColumns).fill(0);
    });
});