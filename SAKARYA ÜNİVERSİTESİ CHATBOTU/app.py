from flask import Flask, render_template, request, jsonify
import os
from google import generativeai as genai
import json

app = Flask(__name__)

# Google Gemini API anahtarını ayarla
API_KEY = "buraya api key giriniz"
genai.configure(api_key=API_KEY)

# JSON dosyasından Sakarya Üniversitesi bilgilerini yükle
def load_sau_info():
    try:
        with open('sau_info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Hata: {str(e)}")
        return None

# Model nesnesi
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    try:
        # SAU bilgilerini yükle
        sau_data = load_sau_info()
        if not sau_data:
            return jsonify({'response': 'Üzgünüm, üniversite bilgilerine şu anda erişemiyorum.'})

        # Bilgileri kategorilere göre formatla
        uni_info = f"""
        Üniversite Hakkında:
        {sau_data['universite_genel']['ad']} hakkında size yardımcı olabilirim.
        
        Genel Bilgiler:
        - Kuruluş: {sau_data['genel_bilgiler']['kurulus_tarihi']['yil']}
        - Rektör: {sau_data['genel_bilgiler']['rektor']}
        - Konum: {sau_data['genel_bilgiler']['konum']}
        - Web Sitesi: {sau_data['genel_bilgiler']['web_sitesi']}
        
        Fakülteler:
        {', '.join(sau_data['akademik_birimler']['fakulteler'])}
        
        Enstitüler:
        {', '.join(sau_data['akademik_birimler']['enstituler'])}
        
        Kampüs Olanakları:
        - {sau_data['kampus_olanaklari']['kutuphane']}
        - {sau_data['kampus_olanaklari']['laboratuvarlar']}
        - {sau_data['kampus_olanaklari']['spor_tesisleri']}
        - {sau_data['kampus_olanaklari']['yemekhane']}
        - {sau_data['kampus_olanaklari']['saglik_hizmetleri']}
        
        Bilgisayar Mühendisliği Bölümü:
        - Bölüm Başkanı: {sau_data['bilgisayar_muhendisligi']['genel_bilgiler']['bolum_baskani']}
        - Web Sitesi: {sau_data['bilgisayar_muhendisligi']['genel_bilgiler']['web_sitesi']}
        - İletişim: {sau_data['bilgisayar_muhendisligi']['genel_bilgiler']['iletisim']['email']}
        """
        
        # Gemini API'yi kullanarak yanıt al
        prompt = f"""Sen Sakarya Üniversitesi'nin resmi chatbot'usun. 
        Aşağıdaki bilgilere dayanarak soruları cevaplayabilirsin:
        
        {uni_info}
        
        Eğer soruda Sakarya Üniversitesi ile ilgili olmayan bir konu sorulursa, 
        nazikçe konuyu Sakarya Üniversitesi ile ilgili bilgilere yönlendir.
        
        Öğrencilere her zaman nazik, bilgilendirici ve yardımcı ol.
        
        Kullanıcının sorusu: {user_message}"""
        
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f'Hata oluştu: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True) 