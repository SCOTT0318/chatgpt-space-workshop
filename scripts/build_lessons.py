"""Inline the visual teaching modules into the buildless public course."""
from pathlib import Path
import re
import json
import zipfile

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

# The course keeps teaching content only; the user removed the timetable.
if '<div class="v-agenda"' in page:
    start = page.index('<div class="v-agenda"')
    end = page.index('<div class="table-wrap schedule">', start)
    page = page[:start] + page[end:]
page = re.sub(r'<details class="lesson-agenda" id="lesson-agenda">.*?</details>\s*', '', page, count=1, flags=re.S)

page = page.replace('PRACTICAL AI FOR YOUR TEAM', 'VISUAL LESSONS / 그림으로 배우는 업무 AI')
page = page.replace('<a class="button primary" href="#practice">실습 시작하기', '<a class="button primary" href="#lesson-how-to">그림으로 배우기')
page = page.replace('회의메모가 실행계획이 되고,<br>매출 데이터가 보고서와 발표자료가 되는 3시간.<br>업무의 시작부터 검토·공유·반복까지 직접 연결합니다.', '개념은 관계도로, 조작은 화면 모식도로,<br>완성 기준은 실제 형태의 결과물 예시로 배웁니다.<br>보고 따라 만들며 업무에 연결하는 3시간입니다.')
page = page.replace('01</span>업무에 AI를 붙이는 법', '01</span>개념도와 프롬프트 해부도')
page = page.replace('02</span>스페이스 기능 안내', '02</span>화면으로 배우는 기능')
page = page.replace('카드를 열면 사용 순서·업무 예시·복사할 요청을 볼 수 있습니다.', '위쪽 화면 모식도로 조작 순서를 익히고, 아래 기능 카드에서 업무 예시와 요청을 찾아보세요.')
page = page.replace('v1.1 · 2026.11.02', 'v1.2 · 2026.11.02')
page = page.replace('v1.2 · 2026.11.02', 'v1.3 · 2026.11.02')
page = page.replace('20개 기능·연결 워크플로와 5단계 실습을 한곳에서 배웁니다.', '기능 사용, 스킬 제작, 팀 프로젝트 공유와 공동 작업을 한곳에서 배웁니다.')

# Remove the selected calculator and its listeners, then make data analysis an
# optional example. The course teaches product use and team work.
calc_marker = '<div class="panel" style="background:var(--tint)"><span class="tag green">교육용 인터랙션 데모</span>'
if calc_marker in page:
    start = page.index(calc_marker)
    end = page.index('<div class="promptbox">', start)
    page = page[:start] + '</div>\n ' + page[end:]
page = re.sub(r'^function calc\(\).*?calc\(\);\s*$', '// Calculator demonstration removed.', page, count=1, flags=re.M)
page = page.replace('<div class="grid2"><div><ol class="steps"><li><b>Slides 직접 만들기 · 12분</b>', '<div class="output-use-steps"><div><ol class="steps"><li><b>Slides 만들기</b>')
page = page.replace('<b>Visualize 시연 · 5분</b><br>계산식을 제시해 달성률 계산기를 요청합니다. 정상값·목표 0·잘못된 입력을 시험합니다.', '<b>Visualize로 업무 절차 설명하기</b><br>문의 접수 → 정책 확인 → 답변 초안 → 담당자 검토의 흐름도를 요청합니다. 단계별 설명이 정확한지 확인합니다.')
page = page.replace('<b>이미지 시연 · 4분</b>', '<b>이미지 만들고 수정하기</b>').replace('<b>Sites 시연 · 4분</b>', '<b>Sites로 업무 안내 만들기</b>')
page = page.replace('계산기 입력을 바꿔 시험하고 사이트의 게시 범위를 설명할 수 있다.', '업무 흐름도와 사이트 예시를 보고 실제 업무에 쓸 곳을 설명할 수 있다.')
page = page.replace('Slides를 만드는 동안 계산기를 시연합니다. 목표를 0으로 바꾸고 왜 예외 처리가 필요한지 묻습니다.', 'Slides를 만드는 동안 같은 내용을 업무 흐름도로 바꾸는 요청을 시연합니다.')
page = page.replace('예산 계산기, 프로세스도, 대안 비교, 화면 시안.', '업무 흐름도, 의사결정 순서, 대안 비교, 화면 시안.')
page = page.replace('현재 검산된 매출과 목표를 초기값으로 한 달성률 계산기를 만들어줘. 두 값을 수정하면 매출÷목표×100을 보여주고 목표가 0이면 계산 불가로 표시해줘. 단위는 원.', '문의 접수 → 정책 확인 → 답변 초안 → 담당자 검토의 업무 흐름도를 만들어줘. 각 단계를 선택하면 입력 자료·담당 역할·완료 기준을 설명해줘.')
page = page.replace('계산기·도식', '업무 흐름도·화면 예시').replace('·계산기·퀴즈', '·도식·퀴즈')
page = page.replace('입력값을 바꾸는 업무 흐름도·화면 예시', '업무 순서를 설명하는 도식·화면 예시')
if 'id="optional-analysis"' not in page:
    start = page.index('<article class="lab" id="lab-data"')
    end = page.index('<article class="lab" id="lab-output"', start)
    example = page[start:end].replace('class="progress-check" data-key="data1"', 'data-key="data1"').replace('class="progress-check" data-key="data2"', 'data-key="data2"')
    page = page[:start] + '<details class="optional-analysis" id="optional-analysis"><summary>선택 사례 · AI에 파일 분석을 요청하고 결과를 검토하는 방법</summary>\n' + example + '</details>\n ' + page[end:]
page = page.replace('실습 ④ · 20분. 결과를 만든 사람과 검토하는 사람을 바꿔 봅니다.', '결과를 만든 사람과 검토하는 사람을 바꾸며 문서를 함께 다듬습니다.')
page = page.replace('실습 ⑤ · 30분. 실제 자료 대신 업무 구조를 적고 합성 자료로 적용안을 만듭니다.', '실제 자료 대신 업무 구조를 적고 합성 자료로 팀 적용안을 만듭니다.')
page = page.replace('<strong>5</strong><span>단계별·종합 실습</span>', '<strong>팀</strong><span>직무별 실습·공동 작업</span>')
page = page.replace('근거가 연결된 실행계획 Page, 검산한 실적표, 5장 발표자료를 만들고 공유 범위와 다음 실행 방법을 설명할 수 있습니다.', '필요한 기능으로 문서를 만들고, 반복 절차의 스킬 초안과 팀 프로젝트를 준비해 공유·검토하는 흐름을 설명할 수 있습니다.')
page = page.replace('예산 계산기, 업무 흐름도', '업무 흐름도').replace('초안, 계산기, 반복 요청', '초안, 업무 도식, 반복 요청')
page = page.replace('이 HTML의 계산기 데모', '화면 모식도와 결과물 예시')
page = re.sub(r'<aside class="instructor"><h4>강사 노트.*?</aside>\s*', '', page, flags=re.S)
page = page.replace('강사 노트', '강사용 해설').replace('진행 메모와 모범답안', '검토 기준과 모범답안').replace('진행 메모와 정답', '검토 기준과 정답')
page = page.replace('휴식 10분 포함', '기능·스킬·협업 실습').replace('마무리 10분 · ', '')
page = re.sub(r'<span class="tag green">\d+분</span>', '', page)
page = re.sub(r' · \d+분', '', page)
step_index=[0]
def renumber_task_steps(match):
    step_index[0]+=1
    return f'>STEP {step_index[0]:02d}<'
page = re.sub(r'>\d+ MIN<',renumber_task_steps,page)

concept = (PARTS / 'concept.html').read_text()
upsert('concept', concept, lambda p,b: before_in_section(p,'basics','<div class="grid2">',b))
upsert('walkthrough', (PARTS / 'walkthrough.html').read_text(), lambda p,b: before_in_section(p,'features','<div class="filters"',b))

examples = (PARTS / 'examples.html').read_text()
page_example, slides_example = examples.split('<!-- SLIDES_EXAMPLE -->', 1)
upsert('page-example', page_example, lambda p,b: before_in_section(p,'lab-page','<div class="grid2">',b))
upsert('slides-example', slides_example, lambda p,b: before_in_section(p,'lab-output','<div class="grid2">',b))
upsert('collaboration', (PARTS / 'collaboration.html').read_text(), lambda p,b: before_in_section(p,'collaboration','<div class="grid3">',b))

skills = '''<section class="chapter" id="skills" aria-labelledby="skills-chapter-title"><div class="section-head"><div><div class="eyebrow">04 / BUILD A REUSABLE SKILL</div><h2 id="skills-chapter-title">반복 업무의 절차를 스킬로 만듭니다.</h2><p class="lead">자연어로 만들고, 예시로 시험하고, 팀에서 다시 쓰는 방법을 익힙니다.</p></div><span class="section-no">04</span></div>'''+(PARTS/'skills.html').read_text()+'''<div class="checklist"><label class="check"><input class="progress-check" data-key="skill1" type="checkbox"><span class="check-text">입력·절차·출력·검토 기준이 있는 스킬 초안을 만들었다.</span></label><label class="check"><input class="progress-check" data-key="skill2" type="checkbox"><span class="check-text">정상 요청·정보 부족·범위 밖 요청으로 시험하고 배포 범위를 구분했다.</span></label></div></section>'''
upsert('skills', skills, lambda p,b:p.replace('<section class="chapter" id="collaboration"',b+'\n<section class="chapter" id="collaboration"',1))
team = '''<section class="chapter" id="team-projects" aria-labelledby="team-chapter-title"><div class="section-head"><div><div class="eyebrow">05 / SHARE CONTEXT, WORK TOGETHER</div><h2 id="team-chapter-title">팀 프로젝트를 공유하고 역할을 나눠 일합니다.</h2><p class="lead">공통 자료·지침·채팅을 모으고, 각자 작업한 결과를 공동 문서로 연결합니다.</p></div><span class="section-no">05</span></div>'''+(PARTS/'team-projects.html').read_text()+'''<div class="checklist"><label class="check"><input class="progress-check" data-key="team1" type="checkbox"><span class="check-text">팀 프로젝트에 공통 지침·자료를 넣고 Owner·Edit·Chat 역할을 확인했다.</span></label><label class="check"><input class="progress-check" data-key="team2" type="checkbox"><span class="check-text">새 채팅·분기로 나눠 작업하고 Space 문서에서 결과를 함께 검토했다.</span></label></div></section>'''
upsert('team-projects', team, lambda p,b:p.replace('<section class="chapter" id="collaboration"',b+'\n<section class="chapter" id="collaboration"',1))

nav = [('start','00','오늘의 목표와 준비'),('basics','01','개념도와 프롬프트'),('features','02','화면으로 배우는 기능'),('practice','03','문서·결과물 만들기'),('skills','04','스킬 만드는 법'),('team-projects','05','팀 프로젝트 공유·협업'),('collaboration','06','공동 검토와 반복 업무'),('challenge','07','우리 팀 업무에 적용'),('prompts','08','직무별 프롬프트'),('assessment','09','이해도와 실천 계획'),('references','10','기능 확인·공식 출처')]
page = re.sub(r'<nav class="nav">.*?</nav>', '<nav class="nav">'+''.join(f'<a href="#{id}"><span>{number}</span>{title}</a>' for id,number,title in nav)+'</nav>', page, count=1, flags=re.S)
page = page.replace("const navIcons=['target','lightbulb','folder','table','users','building','spark','check','book'];", "const navIcons=['target','lightbulb','folder','table','spark','users','comment','building','spark','check','book'];")
for id, number in [('collaboration','06'),('challenge','07'),('prompts','08'),('assessment','09'),('references','10')]:
    page = re.sub(rf'(<section class="chapter" id="{id}".*?<span class="section-no">)\d+(</span>)',rf'\g<1>{number}\2',page,count=1,flags=re.S)
    page = re.sub(rf'(<section class="chapter" id="{id}".*?<div class="eyebrow">)\d+',rf'\g<1>{number}',page,count=1,flags=re.S)

reference_match=re.search(r'(<ul class="source-list">)(.*?)(</ul>)',page,flags=re.S)
extra_sources=[('Build skills','https://learn.chatgpt.com/docs/build-skills'),('Skill controls','https://learn.chatgpt.com/docs/enterprise/skills'),('공유 Projects · 공식 도움말','https://help.openai.com/en/articles/10169521-projects-in-chatgpt')]
source_body=reference_match.group(2)
for title,url in extra_sources:
    if url not in source_body:
        number=source_body.count('<li>')+1
        source_body+=f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{number:02d} · {title} ↗</a></li>'
page=page[:reference_match.start(2)]+source_body+page[reference_match.end(2):]

data_match = re.search(r'(<script id="course-data" type="application/json">)(.*?)(</script>)',page,flags=re.S)
data = json.loads(data_match.group(2))
if len(data['quiz']) == 6:
    data['quiz'][1] = dict(q='02. AI에 업무 문서를 맡기기 전에 무엇을 정해야 하나요?',a=['사용할 근거·결과 형식·검토 기준','보기 좋은 색만 정하기','내용을 확인하지 않고 바로 공유하기'],correct=0,why='목적과 자료, 완성 기준을 먼저 정해야 검토할 수 있는 결과를 만들 수 있습니다.')
    data['quiz'][4] = dict(q='05. 스킬을 만든 뒤 올바른 확인 방법은?',a=['한 번 저장하면 테스트 없이 계속 사용한다.','정상 요청·정보 부족·범위 밖 요청으로 시험한다.','모든 업무에 무조건 실행하게 만든다.'],correct=1,why='스킬이 맡을 범위와 정보가 부족할 때의 동작까지 확인합니다.')
    data['quiz'] += [
        dict(q='07. 프로젝트의 자료·지침은 쓰되 다른 사람을 초대하지 않는 역할은?',a=['Chat','Edit','Owner'],correct=0,why='프로젝트 Chat 권한은 대화와 자료·지침 이용을 위한 역할입니다.'),
        dict(q='08. 동료의 프로젝트 대화를 이어서 다른 방향을 시험하려면?',a=['같은 채팅을 동시에 타이핑한다.','새 채팅 또는 Branch로 분기해 작업한다.','원본 채팅을 지워 버린다.'],correct=1,why='공유 프로젝트는 새 채팅과 분기로 협업합니다. 문서 동시 편집은 Space에서 별도로 공유합니다.'),
        dict(q='09. 프로젝트를 공유하면 만든 스킬도 팀원에게 자동 설치되나요?',a=['언제나 자동 설치된다.','아니다. 지원되는 스킬 공유·배포와 설치를 따로 확인한다.','파일 이름만 같으면 자동 실행된다.'],correct=1,why='프로젝트 맥락 공유와 스킬 배포는 별개입니다.'),
        dict(q='10. 여러 사람이 같은 문서·Slides를 함께 고치려면?',a=['결과물을 Space에서 별도로 공유하고 편집 권한을 확인한다.','프로젝트 채팅을 열면 모든 문서 권한이 생긴다.','원본 링크를 보내면 무조건 수정할 수 있다.'],correct=0,why='프로젝트 접근과 결과물 편집 권한을 각각 확인해야 합니다.'),
    ]
    page=page[:data_match.start(2)]+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+page[data_match.end(2):]
page=page.replace('6문항 · 선택한 뒤 해설을 확인합니다.', '10문항 · 선택한 뒤 해설을 확인합니다.')

quick_links = '''<nav class="lesson-jump" aria-label="시각 수업 자료 바로가기"><b>배우고 싶은 내용</b><a href="#lesson-how-to">기능 사용 순서</a><a href="#skills">스킬 만드는 법</a><a href="#team-projects">팀 프로젝트 공유</a><a href="#le-page-heading">문서 결과 예시</a><a href="#lg-sharing-title">권한·공동 검토</a></nav>'''
upsert('quick-links', quick_links, lambda p,b: before_in_section(p,'start','<div class="callout"><b>오늘의 완료 기준',b))

shared_css = '''
.sidebar{overflow-y:auto}.sidebar .brand,.sidebar .nav{flex-shrink:0}.optional-analysis{margin:22px 0;padding:18px 20px;border:1px solid var(--line);background:#fff;border-radius:12px}.output-use-steps{display:block}.lesson-jump{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:24px 0 18px}.lesson-jump b{font-size:11px;color:#62735a;margin-right:6px}.lesson-jump a{font-size:11px;padding:6px 10px;border:1px solid #d8e1d0;border-radius:6px;background:#fff;text-decoration:none;color:#3e6442}.lesson-jump a:hover{background:#e6efdb}.lesson-jump a:focus-visible{outline:3px solid #7d9f50;outline-offset:3px}.lc-module,.lw-guide,.le-ex,.lg-lesson{scroll-margin-top:90px}body .le-table{min-width:0!important}@media print{.lesson-jump{display:none}}'''
css = shared_css + '\n' + '\n'.join((PARTS / (name+'.css')).read_text() for name in ['concept','walkthrough','examples','collaboration','skills','team-projects'])
upsert('styles', '<style>\n'+css+'\n</style>', lambda p,b: p.replace('</head>',b+'\n</head>',1))
js = '\n'.join((PARTS / (name+'.js')).read_text() for name in ['concept','walkthrough','examples','skills','team-projects'])
upsert('scripts', '<script>\n'+js+'\n</script>', lambda p,b: p.replace('</body>',b+'\n</body>',1))
(ROOT / 'index.html').write_text(page)
skill_folder=ROOT/'downloads/meeting-followup-skill'
with zipfile.ZipFile(ROOT/'downloads/meeting-followup-skill.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(skill_folder.rglob('*')):
        if file.is_file(): archive.write(file,str(file.relative_to(skill_folder.parent)))
print(f'Visual course built: {len(page.encode()):,} bytes')
