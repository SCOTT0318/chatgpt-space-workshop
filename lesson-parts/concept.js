(()=>{'use strict';
const root=document.getElementById('lv-concept-prompt');if(!root)return;
const parts={
 purpose:['01','목적 · 누가 무엇을 결정하나요?','청중과 필요한 결정을 알려주면, 같은 자료도 그 사람이 사용할 수 있는 순서와 깊이로 정리할 수 있습니다.','누구에게 필요한지 모르는 일반적인 요약으로 끝나기 쉽습니다.'],
 source:['02','근거 · 어떤 자료를 믿고 쓰나요?','사용할 파일과 범위를 지정하면 결과를 원본으로 대조할 수 있습니다. 이 예시는 먼저 검산한 매출표를 사용합니다.','일반 지식과 회사 자료가 섞이거나, 검산하지 않은 숫자를 재사용할 수 있습니다.'],
 output:['03','결과 · 무엇이 나오면 끝인가요?','문서 길이와 과제 표의 열을 정하면 검토할 산출물이 선명해집니다. 필요한 출력 형식도 함께 요청합니다.','읽기 좋은 설명은 나와도 담당자와 기한이 있는 실행계획이 빠질 수 있습니다.'],
 standard:['04','기준 · 어떤 내용을 확인하나요?','자료에 없는 내용은 미확인으로 남기도록 요청합니다. 사람이 원본과 대조할 항목도 분명해집니다.','빠진 담당자·기한·원인을 자연스러운 문장으로 채워 넣었는지 놓치기 쉽습니다.'],
 review:['05','검토 · 어디에서 사람이 확인하나요?','초안 작성과 실제 발송을 나눕니다. 고객과의 약속이 되기 전에 담당자가 가격·할인·납기를 확인합니다.','초안의 미확인 조건이 실제 약속이나 외부 발송으로 이어질 수 있습니다.']
};
root.querySelectorAll('[data-lc-part]').forEach(button=>button.addEventListener('click',()=>{
 const part=parts[button.dataset.lcPart];if(!part)return;
 root.querySelectorAll('[data-lc-part]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 ['number','title','why','without'].forEach((key,i)=>document.getElementById('lv-concept-part-'+key).textContent=part[i]);
 root.dataset.activePart=button.dataset.lcPart;
}));
})();
