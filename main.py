from flask import Flask
from flask import request
from flask import jsonify
import requests
import subprocess

app = Flask(__name__)

@app.route('/image/create', methods=['GET'])
def create_image():
  prompt = request.args.get('p')
  output = subprocess.run(['ls', '-l'])
  print(output)
  # cookies = {}
  # requests.get(f"https://www.bing.com/images/create?q={prompt}&rt=4&FORM=GENCRE", cookies=cookies)
  
  # return render(request, '')

def main():
  app.run(port=8001)

if __name__ == '__main__':
  output = subprocess.run([
      'python',
      '-m',
      'BingImageCreator',
      '-U',
      '19TUgTuQeLpOGAhqHwUtzq-YUrRnIh2qgxvJMgvrkA6Qoe7a0H38-mC2iCclafjJ-g4Oqk22qdRGjUME8PQAPBrgZh9tGdGohQzbAWurho75vGegz_cfhw2avJJ3hm7gMR8fRBqSusG96NMNC692eA-sN_RgBCAmDHZuOEjhBDecd5SmVLzq0kgoycHUXdanw6TTsWlB0xUNaO2VGBDX2svkCCiAudnd45LSDozAapE8',
      '--prompt',
      'کاور آلبوم آهنگ با موضوع بهار، نوروز،نوروز ۱۴۰۲',
      '--output-dir',
      './output'
    ])
  print(output)
  main()