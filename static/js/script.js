document.getElementById('verifyForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const serialNumber = document.getElementById('serialNumber').value;
    const resultElement = document.getElementById('result');
    const imageElement = document.getElementById('image');
    const descriptionElement = document.getElementById('description');

    resultElement.innerText = '验证中...';
    imageElement.style.display = 'none';
    descriptionElement.style.display = 'none';

    try {
        const response = await fetch('/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ serialNumber: serialNumber })
        });
        const result = await response.json();

        resultElement.innerText = result.message;
        if (response.ok) {
            imageElement.src = result.imageUrl;
            imageElement.style.display = 'block';
            descriptionElement.innerText = result.description;
            descriptionElement.style.display = 'block';
        } else {
            resultElement.innerText = '编号无效';
        }
    } catch (error) {
        resultElement.innerText = '请求失败，请稍后重试';
        console.error('Error:', error);
    }
});
