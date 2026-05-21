const nodemailer = require('nodemailer');

const SMTP_USER = process.env.SMTP_USER || 'wwwfrolof@yandex.ru';
const SMTP_PASS = process.env.SMTP_PASS;
const TO_EMAIL  = process.env.TO_EMAIL  || 'wwwfrolof@yandex.ru';

module.exports = async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { name, phone } = req.body || {};
  if (!name && !phone) return res.status(400).json({ error: 'Заполните хотя бы одно поле' });

  if (!SMTP_PASS) {
    console.error('SMTP_PASS не задан');
    return res.status(500).json({ error: 'Server misconfiguration' });
  }

  const transporter = nodemailer.createTransport({
    host: 'smtp.yandex.ru',
    port: 465,
    secure: true,
    auth: { user: SMTP_USER, pass: SMTP_PASS },
  });

  const text = [
    '=== Новая заявка с сайта психоаналитик-психолог.рф ===',
    '',
    name  ? `Имя: ${name}` : null,
    phone ? `Телефон: ${phone}` : null,
    '',
    `Дата: ${new Date().toLocaleString('ru-RU', { timeZone: 'Asia/Novosibirsk' })}`,
  ].filter(l => l !== null).join('\n');

  try {
    await transporter.sendMail({
      from: `"Сайт Кати" <${SMTP_USER}>`,
      to: TO_EMAIL,
      subject: `Новая заявка от ${name || phone}`,
      text,
    });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Mail error:', err.message);
    return res.status(500).json({ error: 'Не удалось отправить письмо' });
  }
};
