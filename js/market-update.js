(function(root){
  const parseReportWeek=value=>{const match=String(value||'').trim().match(/^(\d{2})\/(\d{2})\/(\d{4})\s*-\s*(\d{2})\/(\d{2})\/(\d{4})$/);if(!match)throw Error('Tuần báo cáo phải có dạng dd/mm/yyyy - dd/mm/yyyy.');const [,sd,sm,sy,ed,em,ey]=match,start=`${sy}-${sm}-${sd}`,end=`${ey}-${em}-${ed}`;if(start>end)throw Error('Ngày bắt đầu phải trước hoặc bằng ngày kết thúc.');return{start,end}};
  const mergeMarketUpdate=(current,update)=>({...current,report:{...current.report,update_date:update.meta.updated_at,source:update.meta.source},indices:update.indices,trading_value:update.trading_value,foreign_flow:update.foreign_flow,top_buy:update.top_buy,top_sell:update.top_sell});
  const api={parseReportWeek,mergeMarketUpdate};
  root.MarketUpdate=api;
  if(typeof module!=='undefined')module.exports=api;
})(globalThis);
