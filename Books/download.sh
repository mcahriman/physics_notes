#!/bin/bash
# Download the source textbooks into the project.
#   ./Books/download.sh            the three Кучерук volumes -> Books/raw/kucheruk{1,2,3}.pdf (checksummed)
#   ./Books/download.sh --library  also the rest of the course reading list -> Books/library/
# Scans are not kept in git (see README); this script recreates them.
set -euo pipefail
cd "$(dirname "$0")"

gdrive() { # gdrive <file-id> <output path>
  curl -fL --retry 3 -o "$2.part" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"
  mv "$2.part" "$2"
}

mkdir -p raw
while read -r id name sum; do
  if [ -f "raw/$name" ] && echo "$sum  raw/$name" | sha256sum -c --quiet 2>/dev/null; then
    echo "ok      raw/$name"; continue
  fi
  echo "fetch   raw/$name"
  gdrive "$id" "raw/$name"
  echo "$sum  raw/$name" | sha256sum -c --quiet || { echo "checksum mismatch: raw/$name" >&2; exit 1; }
done <<'EOF'
19uhoPMBwppprxBSnwpxsMrh9Ef8e4B1I kucheruk1.pdf 6f13aa3c441e36dd339bf2d45157947c8301a4f92abb0eae242f998173d60994
1TRVxqHhyCZrrGaBDl2AVPOMbfae3huvV kucheruk2.pdf 030c27e150a87b33bb759aad4cbf6ea68410ba16d9dcf0aa83549fc1d14ca3b0
104esSlty3Vaa5wPoMESn34nZPP8M0dp8 kucheruk3.pdf 6a0dc73a2788c11f6a716b942b6cd117edde04743ae7f848ce7a3fa8a27a2e9f
EOF

[ "${1:-}" = "--library" ] || exit 0

# The rest of the reading list (no checksums; files can change upstream). Skips files already present.
mkdir -p library
while IFS='|' read -r kind ref name; do
  [ -z "$kind" ] && continue
  [ -s "library/$name" ] && { echo "ok      library/$name"; continue; }
  echo "fetch   library/$name"
  if [ "$kind" = drive ]; then gdrive "$ref" "library/$name" || echo "FAILED  library/$name" >&2
  else curl -fL --retry 3 -o "library/$name" "$ref" || echo "FAILED  library/$name" >&2; fi
done <<'EOF'
url|http://physics.zfftt.kpi.ua/repository/coursefilearea/file.php/1/Labs/Errors/Pogreshnosti.pdf|Лаванов_Бордюг_Сліпухіна_Теорія_похибок_2012.pdf
drive|1Q9A9wmy8rSDsYLBrnzqTnGmQroiijyq0|Білинський_Теорія_ядра_2021__або_Булавін_Молекулярна_фізика.pdf
drive|1N-BbEOiL6VxUQS1abGdUd8ItxPNmGuj5|Каденко_Плюйко_Фізика_атомного_ядра_та_частинок_2019.pdf
url|http://physics.zfftt.kpi.ua/repository/coursefilearea/file.php/1/Labs/Errors/%D0%A1%D0%B0%D0%B2%D1%87%D0%B5%D0%BD%D0%BA%D0%BE.pdf|Савченко_Методичні_вказівки_лабораторні_2023.pdf
drive|1UerpRfMoilS7M2EoEhvkAmNBGmV464oY|Бовтрук_та_ін_Фізика_Механіка_Молекулярна_2017.pdf
drive|1scZb30R4xpkrGtSPa_eOz5z_TEBZyijc|Горобець_Фізика_Механіка_2018.pdf
drive|15-w4tbVpilVpgJjmM-3cFrD7L-ptyhva|Дубовик_Сухов_Лекції_з_механіки_2019.pdf
drive|1nBlmpAWurzihaJ9-kH88e2spfWoG370m|Андріяшик_Вербицький_Король_Фізика_2008.pdf
drive|1faIBevPzo84gDqHk2WETSbeu_l1zMmSH|Бурий_Цогла_Педагогічні_технології_2022.pdf
drive|1c-EWIVM2Fj9BvaTG7Wc3AmV8AN8C8Y2t|Долгих_Астрономія_компетентності_2020.pdf
drive|1npcSbgQhMDlDoW9jQ5Ag1vfSJFB9QO7X|Крячко_Методика_навчання_астрономії_2018.pdf
drive|11j5ThdPxAkYh3LNM1G0IAxSo3V2DeL9R|Иродов_Задачи_по_общей_физике.pdf
drive|1L9HCZojzzaEjKIiW1v8sY02zfQk2NN6F|Иродов_Основные_законы_механики.pdf
drive|1ZwFmClToVRBNRETvx2WO5T3Y8NDyZa-N|Иродов_Основные_законы_электромагнетизма.pdf
drive|1_b35YNelav165Vr_-oCv94Y4dZ2M41XY|Иродов_Волновые_процессы.pdf
drive|1-CcP7JJsSN9v1ieAqcre8iEcpNC61dzx|Иродов_Квантовая_физика.pdf
drive|1AfjUn0bvJegO2Lixanupmdcq8ZLNShSM|Иродов_Физика_макросистем.pdf
drive|1XU854lJI2sVhNrbNyUpPcqSTTNnRtv_K|Дідух_Електрика_і_магнетизм_2021.pdf
drive|1N08fDOVkuieKFM5-jClEdleAsO_dkjQm|Берклеевский_курс_Механика.pdf
drive|1pPv0HqS8o0UfJNeJ1NO1m5YcY0pt4wKq|Берклеевский_курс_Парселл_Электричество_и_магнетизм.pdf
drive|14Om9yipBAQ3JXHA26HHaySRRDg3Ngp2J|Берклеевский_курс_Крауфорд_Волны.pdf
drive|10TD_ASpGpoEmq9T4t4Tu6uYHWk_QnT7X|Берклеевский_курс_Вихман_Квантовая_физика.pdf
drive|1epAp5nrtQcfAG_T8C8xQN2qeKAcawDF7|Берклеевский_курс_Рейф_Статистическая_физика.pdf
drive|1WxKbVcKr1ByX6ztuq9sILg7C1BBi9qpk|Ландау_Лифшиц_т1_Механика.pdf
drive|13ISO5WZBk0BnF3mSp8xEPDur0pGuf0zl|Ландау_Лифшиц_т3_Квантовая_механика.pdf
drive|1R5iC9-gdoIXhAgiaD1J3a2x6msOayuVu|Ландау_Лифшиц_т4_Квантовая_электродинамика.pdf
drive|1sMEH_8QviSOd6ZGu4oS7AkRoNG8cvPnq|Ландау_Лифшиц_т5_Статистическая_физика.pdf
drive|1kWFrr_VXctuBBBsldea8tCbkM4nOu4uN|Landau_Lifshitz_v5_Statistical_Physics_EN.pdf
drive|1VPwrB1ZdT_pVScsiVcu0BGnwrYcwsIdm|Ландау_Лифшиц_т6_Гидродинамика.pdf
drive|1L1Y4bWnbn1LUjLDVuzEdR897HT8OXqqH|Ландау_Лифшиц_т7_Теория_упругости.pdf
drive|1T6m7wPtD3hZf3sJjQtKyZwMuSYz6xsP4|Ландау_Лифшиц_т8_Электродинамика_сплошных_сред.pdf
drive|1f8Ku08ZcsnwZhsBRcIwX-3GADGExPsjh|Ландау_Лифшиц_т9_Статистическая_физика_ч2.pdf
drive|1G5ovI483uw8VrIkCtIlMjfRyYfG84E5d|Ландау_Лифшиц_т10_Физическая_кинетика.pdf
drive|1bycQY0134kXnxtU70VoTKDjLOdgu6Mfe|Bazarov_Thermodynamics_1964.pdf
drive|1Z26ievsQ8imyBtrWa4UY7KEVlycOxT0U|Физическая_энциклопедия_т1.pdf
drive|1TfAFQGNlA_qWAnWpbQs3KMR-B5-r7CC2|Физическая_энциклопедия_т2.pdf
drive|182TD5b0yDueJB91qkst2Nk1Yyg8w0WM_|Физическая_энциклопедия_т3.pdf
drive|11fs8lJ5fbq7Mnqxf_zQSANYTF2tVtHJi|Физическая_энциклопедия_т4.pdf
drive|1ITThERM3gaXAR-rV7lVN_1-sbztdgS7S|Физическая_энциклопедия_т5.pdf
drive|1aUkHqWuu0RcqRzETZneBr6-pHhkgoXvq|Горелик_Кто_изобрел_современную_физику.pdf
drive|1SWYUOarDUNHqXYoGcuehnfQRcG64ukhF|Трофимова_Фирсов_Курс_физики_Задачи_2011.pdf
EOF
