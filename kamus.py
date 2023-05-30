import os

mypath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kamus/')

with open(os.path.join(mypath, 'daftar nama hari dan bulan.txt'), 'r') as f:
  hari_bulan = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar satuan.txt'), 'r') as f:
  satuan = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar kenampakan alam.txt'), 'r') as f:
  kenampakan_alam = [line.strip().casefold() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar kata tugas.txt'), 'r') as f:
  kata_tugas = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar anak dari.txt'), 'r') as f:
  anak_dari = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar istilah agama.txt'), 'r') as f:
  istilah_agama = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar suku bangsa.txt'), 'r', encoding="utf8") as f:
  suku_bangsa = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar bahasa aksara.txt'), 'r') as f:
  bahasa_aksara = [line.strip() for line in f.readlines()]

with open(os.path.join(mypath, 'daftar gelar.txt'), 'r') as f:
  gelar = [line.strip() for line in f.readlines()]
  gelar_lower = [line.lower() for line in gelar]
