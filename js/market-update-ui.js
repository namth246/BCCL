(function(){
  const button=document.querySelector('#update-market-button');
  const status=document.querySelector('#status');
  const isArrayIndex=value=>/^\d+$/.test(value);

  function setFormValue(target,path,value){
    const keys=path.split('.');
    let node=target;
    keys.forEach((key,index)=>{
      const last=index===keys.length-1;
      if(last){node[key]=value;return}
      const nextIsArray=isArrayIndex(keys[index+1]);
      node[key]??=nextIsArray?[]:{};
      node=node[key];
    });
  }

  function currentReportData(){
    const current={};
    document.querySelectorAll('[data-path]').forEach(field=>{
      const value=field.type==='number'?Number(field.value):field.value;
      setFormValue(current,field.dataset.path,value);
    });
    return current;
  }

  async function updateMarketData(){
    try{
      if(location.protocol==='file:')throw Error('Hãy mở báo cáo qua http://127.0.0.1:8000, không mở trực tiếp tệp HTML.');
      const {start,end}=MarketUpdate.parseReportWeek(document.querySelector('#f-report-week').value);
      button.disabled=true;
      button.textContent='Đang cập nhật…';
      status.textContent='Đang lấy dữ liệu thị trường từ vnstock…';
      const response=await fetch(`${MARKET_UPDATE_ENDPOINT}?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`);
      const update=await response.json();
      if(!response.ok)throw Error(update.error||'Không thể lấy dữ liệu thị trường.');
      localStorage.setItem(STORAGE_KEY,JSON.stringify(MarketUpdate.mergeMarketUpdate(currentReportData(),update)));
      status.textContent='Đã cập nhật dữ liệu thị trường. Đang tải lại báo cáo…';
      window.setTimeout(()=>location.reload(),250);
    }catch(error){
      status.textContent=`Không thể cập nhật dữ liệu: ${error.message}`;
      button.disabled=false;
      button.textContent='Cập nhật dữ liệu';
    }
  }

  button?.addEventListener('click',updateMarketData);
})();
