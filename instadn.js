addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

// متغیر محیطی TELEGRAM_TOKEN از Cloudflare
const TELEGRAM_TOKEN = TELEGRAM_TOKEN
const TELEGRAM_API = `https://api.telegram.org/bot${TELEGRAM_TOKEN}`

// دریافت درخواست از تلگرام
async function handleRequest(request) {
  if (request.method === 'POST') {
    const body = await request.json()

    if (body.message && body.message.text) {
      const chat_id = body.message.chat.id
      const text = body.message.text.trim()

      if (text.includes('instagram.com')) {
        try {
          const api_url = `https://ssyoutube.com/api/convert?url=${encodeURIComponent(text)}`
          const resp = await fetch(api_url)
          const data = await resp.json()

          let reply = '❌ چیزی پیدا نشد.'
          if (data.medias && data.medias.length > 0) {
            reply = `✅ لینک دانلود:\n${data.medias[0].url}`
          }

          await sendMessage(chat_id, reply)
        } catch (err) {
          await sendMessage(chat_id, `❌ خطا: ${err}`)
        }
      } else {
        await sendMessage(chat_id, '⚠️ لطفاً لینک معتبر اینستاگرام بده.')
      }
    }
    return new Response('ok')
  }
  return new Response('Telegram Worker is running!')
}

// ارسال پیام به کاربر
async function sendMessage(chat_id, text) {
  await fetch(`${TELEGRAM_API}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id, text })
  })
}
