"""Inline the visual teaching modules into the buildless public course."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'lesson-parts'
page = (ROOT / 'index.html').read_text()

def upsert(name, content, insert):
    global page
    block = f'<!-- LESSON:{name}:START -->\n{content}\n<!-- LESSON:{name}:END -->'
    pattern = rf'<!-- LESSON:{name}:START -->.*?<!-- LESSON:{name}:END -->'
    if re.search(pattern, page, flags=re.S):
        page = re.sub(pattern, lambda _: block, page, count=1, flags=re.S)
    else:
        page = insert(page, block)

def before_in_section(text, section_id, marker, block):
    start = text.index(f'id="{section_id}"')
    position = text.index(marker, start)
    return text[:position] + block + '\n' + text[position:]

# Keep the timetable as a compact facilitator reference; teaching visuals belong
# beside the concepts and exercises they explain.
if '<div class="v-agenda"' in page:
    start = page.index('<div class="v-agenda"')
    end = page.index('<div class="table-wrap schedule">', start)
    page = page[:start] + page[end:]
if 'id="lesson-agenda"' not in page:
    start = page.index('<div class="spacer"></div><div class="section-head"><div><h3>3시간 운영안</h3>')
    end = page.index('<div class="grid2 mt">', start)
    table_start = page.index('<div class="table-wrap schedule">', start)
    table = page[table_start:end].strip()
    page = page[:start] + '<details class="lesson-agenda" id="lesson-agenda"><summary>3시간 진행표 보기 · 휴식 10분 포함</summary>' + table + '</details>\n ' + page[end:]

page = page.replace('PRACTICAL AI FOR YOUR TEAM', 'VISUAL LESSONS / 그림으로 배우는 업무 AI')
page = page.replace('<a class="button primary" href="#practice">실습 시작하기', '<a class="button primary" href="#lesson-how-to">그림으로 배우기')
page = page.replace('회의메모가 실행계획이 되고,<br>매출 데이터가 보고서와 발표자료가 되는 3시간.<br>업무의 시작부터 검토·공유·반복까지 직접 연결합니다.', '개념은 관계도로, 조작은 화면 모식도로,<br>완성 기준은 실제 형태의 결과물 예시로 배웁니다.<br>보고 따라 만들며 업무에 연결하는 3시간입니다.')
page = page.replace('01</span>업무에 AI를 붙이는 법', '01</span>개념도와 프롬프트 해부도')
page = page.replace('02</span>스페이스 기능 안내', '02</span>화면으로 배우는 기능')
page = page.replace('카드를 열면 사용 순서·업무 예시·복사할 요청을 볼 수 있습니다.', '위쪽 화면 모식도로 조작 순서를 익히고, 아래 기능 카드에서 업무 예시와 요청을 찾아보세요.')
page = page.replace('v1.1 · 2026.11.02', 'v1.2 · 2026.11.02')

concept = (PARTS / 'concept.html').read_text()
upsert('concept', concept, lambda p,b: before_in_section(p,'basics','<div class="grid2">',b))
upsert('walkthrough', (PARTS / 'walkthrough.html').read_text(), lambda p,b: before_in_section(p,'features','<div class="filters"',b))

examples = (PARTS / 'examples.html').read_text()
page_example, slides_example = examples.split('<!-- SLIDES_EXAMPLE -->', 1)
upsert('page-example', page_example, lambda p,b: before_in_section(p,'lab-page','<div class="grid2">',b))
upsert('slides-example', slides_example, lambda p,b: before_in_section(p,'lab-output','<div class="grid2">',b))
upsert('collaboration', (PARTS / 'collaboration.html').read_text(), lambda p,b: before_in_section(p,'collaboration','<div class="grid3">',b))

quick_links = '''<nav class="lesson-jump" aria-label="시각 수업 자료 바로가기"><b>수업 그림 바로 보기</b><a href="#lv-concept-map">개념 관계도</a><a href="#lv-concept-prompt">프롬프트 해부도</a><a href="#lesson-how-to">6단계 사용 화면</a><a href="#le-page-heading">회의록 전후 비교</a><a href="#le-slides-heading">5장 발표자료 예시</a><a href="#lg-sharing-title">권한·예약 도식</a></nav>'''
upsert('quick-links', quick_links, lambda p,b: before_in_section(p,'start','<div class="callout"><b>오늘의 완료 기준',b))

shared_css = '''
.lesson-agenda{margin:28px 0;padding:17px 20px;border:1px solid var(--line);border-radius:11px;background:#fff}.lesson-agenda>summary{font-size:13px}.lesson-jump{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:24px 0 18px}.lesson-jump b{font-size:11px;color:#62735a;margin-right:6px}.lesson-jump a{font-size:11px;padding:6px 10px;border:1px solid #d8e1d0;border-radius:6px;background:#fff;text-decoration:none;color:#3e6442}.lesson-jump a:hover{background:#e6efdb}.lesson-jump a:focus-visible{outline:3px solid #7d9f50;outline-offset:3px}.lc-module,.lw-guide,.le-ex,.lg-lesson{scroll-margin-top:90px}body .le-table{min-width:0!important}@media print{.lesson-jump{display:none}.lesson-agenda{break-inside:avoid}.lesson-agenda>summary{font-size:10pt}}'''
css = shared_css + '\n' + '\n'.join((PARTS / (name+'.css')).read_text() for name in ['concept','walkthrough','examples','collaboration'])
upsert('styles', '<style>\n'+css+'\n</style>', lambda p,b: p.replace('</head>',b+'\n</head>',1))
js = '\n'.join((PARTS / (name+'.js')).read_text() for name in ['concept','walkthrough','examples'])
upsert('scripts', '<script>\n'+js+'\n</script>', lambda p,b: p.replace('</body>',b+'\n</body>',1))
(ROOT / 'index.html').write_text(page)
print(f'Visual course built: {len(page.encode()):,} bytes')
