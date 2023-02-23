"use strict";(self["webpackChunktodo_front"]=self["webpackChunktodo_front"]||[]).push([[997],{8590:function(e,t,a){a.r(t),a.d(t,{default:function(){return te}});var s=a(6252),l=a(2262),i=a(3577),n=a(9963),d=a(3392),o=a(3100),c=a(9980),u=a.n(c),r=a(5762);const k={id:"loading"};function h(e,t){return(0,s.wg)(),(0,s.iD)("div",k)}var v=a(3744);const p={},g=(0,v.Z)(p,[["render",h],["__scopeId","data-v-1a8d99b9"]]);var y=g,_=a(9876),m=(a(7658),a(9669)),S=a.n(m);function w(){let e=JSON.parse(localStorage.getItem("user"));return e&&e["access"]?{Authorization:"Bearer "+e.access}:{}}const f=(0,_.Q_)("tasks",{state:()=>({display:!1,tasksList:[],tasksSlice:[],date:(new Date).toISOString().slice(0,10),enteredText:"",editedText:"",invalidInput:!1,isLoading:!1}),actions:{async loadTasks(){this.isLoading=!0;try{const e=await S().get("task/",{headers:w()}),t=e.data,a=[];return t.forEach((e=>{if(!a.filter((t=>t["date"]===e.date)).length>0)a.push({date:e.date,tasks:[{...e,editable:!1}]});else{const t=a.findIndex((t=>t.date===e.date));a[t].tasks.push({...e,editable:!1})}})),this.isLoading=!1,console.log("Load..."),a}catch(e){console.log(e)}},loadOneTask(e){0===this.tasksList.filter((t=>t["date"]===e)).length?(this.display=!1,this.tasksSlice=[]):(this.tasksSlice=this.tasksList.filter((t=>t["date"]===e))[0],this.display=!0,this.tasksSlice.tasks.sort(((e,t)=>e.priority>t.priority?1:t.priority>e.priority?-1:0)))},async checkUncheck(e){try{await S().patch("task/"+e.task_id,{completed:!e.completed},{headers:w()}),console.log("Completed!"),this.tasksList=await this.loadTasks(),this.loadOneTask(this.date)}catch(t){console.log(t)}},async addNewTask(){const e="date"in this.tasksSlice?this.tasksSlice.tasks.length+1:1;if(""!==this.enteredText)try{await S().post("task/",{priority:e,date:this.date,text:this.enteredText,completed:!1},{headers:w()}),console.log("Added!"),this.tasksList=await this.loadTasks(),this.loadOneTask(this.date),this.enteredText=""}catch(t){console.log(t)}else this.invalidInput=!0},clearInvalidInput(){this.invalidInput=!1},async deleteTask(e){try{await S()["delete"]("task/"+e.task_id,{headers:w()}),console.log("Deleted!"),this.tasksList=await this.loadTasks(),this.loadOneTask(this.date)}catch(t){console.log(t)}this.updatePriority()},async updatePriority(){const e={};for(const a in this.tasksSlice.tasks)this.tasksSlice.tasks[a].priority!==Number(a)+1&&(e[this.tasksSlice.tasks[a].task_id]=Number(a)+1);if(Object.keys(e).length>0){const a={};a["update"]=e;try{await S().patch("task/update/order",{...a},{headers:w()}),console.log("Multiple Rows Update!")}catch(t){console.log(t)}this.tasksList=await this.loadTasks(),this.loadOneTask(this.date)}},async applyEditChanges(e){if(this.editedText&&this.editedText!==e.text)try{await S().patch("task/"+e.task_id,{text:this.editedText},{headers:w()}),console.log("Edited!"),this.tasksList=await this.loadTasks(),this.loadOneTask(this.date)}catch(t){console.log(t)}}}});var T=a(9763),U=a(2791);const x=e=>((0,s.dD)("data-v-d79199f4"),e=e(),(0,s.Cn)(),e),b={class:"grid-container"},I={class:"grid-item-todo"},D={key:0,class:"no-tasks",style:{display:"flex","flex-direction":"column"}},C=x((()=>(0,s._)("h2",null,"No Tasks to Display",-1))),L={key:1},O={class:"unselectable"},z={class:"flex-headers"},N=x((()=>(0,s._)("div",{class:"header-number"},"#",-1))),E=x((()=>(0,s._)("div",{class:"header-text"},"Description",-1))),H={class:"header-edit"},P={class:"header-delete"},B=x((()=>(0,s._)("div",{class:"header-completed"},"Status",-1))),M={class:"flexbox"},W={class:"flex-id"},q=["onDblclick"],A=["contenteditable","onBlur"],F=["onMouseover"],V=["onClick"],Z=["onClick"],j=["onClick","src"],J=x((()=>(0,s._)("button",{class:"button-74"},"add task",-1))),K={key:2,class:"invalid-input"},Q={class:"grid-item-calendar"},R={key:0,class:"task-status"},Y={id:"total-tasks"},G={id:"complete-tasks"},X={id:"uncomplete-tasks"};var $={__name:"TheTasks",setup(e){(0,T.t)();const t=f(),{display:c,tasksList:k,tasksSlice:h,date:v,invalidInput:p,enteredText:g,editedText:m,isLoading:S}=(0,_.Jk)(t),w=(0,l.iH)(null),x=(0,l.iH)(null),$=(0,l.iH)(null),ee=(0,l.iH)(null);function te(e){return e.toLocaleDateString("en-US",{month:"long",year:"numeric",day:"numeric"})}h.value.length>0&&(x.value=h.value.tasks.filter((e=>!e.completed)).length),(0,s.bv)((async()=>{k.value=await t.loadTasks(),t.loadOneTask(v.value)})),(0,s.YP)([h],(()=>{"date"in h.value?(ee.value=h.value.tasks.length,x.value=h.value.tasks.filter((e=>!e.completed)).length,$.value=ee.value-x.value):(ee.value=null,$.value=null,x.value=null)}));const ae=e=>{v.value=e.toISOString().slice(0,10),h.value=k.value.filter((e=>e["date"]===v.value))[0],c.value=!0,h.value||(h.value=(0,l.iH)([]),c.value=!1),t.loadOneTask(v.value)};function se(e){m.value=e.target.innerText}function le(e){h.value.tasks.forEach(((t,a)=>{e.task_id==t.task_id&&(h.value.tasks[a].editable=!h.value.tasks[a].editable)}))}const ie=(0,l.iH)([a(6697),a(2160)]);return(e,a)=>{const k=(0,s.up)("the-header"),_=(0,s.up)("the-footer");return(0,s.wg)(),(0,s.iD)("div",b,[(0,s.Wm)(k,{class:"header"}),(0,s._)("div",I,[(0,s.Wm)(r.Z,null,{default:(0,s.w5)((()=>[(0,l.SU)(c)||(0,l.SU)(S)?((0,s.wg)(),(0,s.iD)("div",L,[(0,s._)("h1",O,(0,i.zw)("Invalid Date"!==te(new Date((0,l.SU)(h).date))?te(new Date((0,l.SU)(h).date)):""),1),(0,s._)("div",z,[N,E,(0,s.wy)((0,s._)("div",H,"Edit",512),[[n.F8,w.value]]),(0,s.wy)((0,s._)("div",P,"Del.",512),[[n.F8,w.value]]),B])])):((0,s.wg)(),(0,s.iD)("div",D,[(0,s._)("div",null,(0,i.zw)(te(new Date((0,l.SU)(v)))),1),C])),(0,s.Wm)((0,l.SU)(u()),{list:(0,l.SU)(h).tasks,"item-key":"task_id",onChange:(0,l.SU)(t).updatePriority},{item:(0,s.w5)((({element:e})=>[(0,s._)("div",M,[(0,s._)("div",W,[(0,s._)("p",null,(0,i.zw)(e.priority),1)]),(0,s._)("div",{class:(0,i.C_)(["flex-text",{editSelectedBorder:e.editable}]),onDblclick:a=>(0,l.SU)(t).checkUncheck(e)},[(0,s._)("p",{contenteditable:e.editable,onInput:se,onBlur:a=>(0,l.SU)(t).applyEditChanges(e)},(0,i.zw)(e.text),41,A)],42,q),(0,s._)("div",{class:"flex-buttons",onMouseover:t=>w.value=e.priority,onMouseout:a[0]||(a[0]=e=>w.value=null)},[(0,s.wy)((0,s._)("img",{src:d,class:(0,i.C_)(["edit-img",{editSelected:e.editable}]),onClick:t=>le(e)},null,10,V),[[n.F8,w.value===e.priority]]),(0,s.wy)((0,s._)("img",{src:o,alt:"delete-image",class:"delete-img",onClick:a=>(0,l.SU)(t).deleteTask(e)},null,8,Z),[[n.F8,w.value===e.priority]]),(0,s._)("img",{onClick:a=>(0,l.SU)(t).checkUncheck(e),src:e.completed?ie.value[0]:ie.value[1],alt:"status",class:"status-img"},null,8,j)],40,F)])])),_:1},8,["list","onChange"]),(0,s._)("div",null,[(0,l.SU)(S)?((0,s.wg)(),(0,s.j4)(y,{key:1})):((0,s.wg)(),(0,s.iD)("form",{key:0,class:"form-control",onSubmit:a[4]||(a[4]=(0,n.iM)(((...e)=>(0,l.SU)(t).addNewTask&&(0,l.SU)(t).addNewTask(...e)),["prevent"]))},[(0,s.wy)((0,s._)("input",{class:"task-input",onBlur:a[1]||(a[1]=(...e)=>(0,l.SU)(t).clearInvalidInput&&(0,l.SU)(t).clearInvalidInput(...e)),onKeyup:a[2]||(a[2]=(...e)=>(0,l.SU)(t).clearInvalidInput&&(0,l.SU)(t).clearInvalidInput(...e)),"onUpdate:modelValue":a[3]||(a[3]=e=>(0,l.dq)(g)?g.value=e:null),type:"text","aria-label":"Add task"},null,544),[[n.nr,(0,l.SU)(g)]]),J],32))]),(0,l.SU)(p)?((0,s.wg)(),(0,s.iD)("span",K,"Please Enter Text")):(0,s.kq)("",!0)])),_:1})]),(0,s._)("div",Q,[(0,s._)("h1",null,(0,i.zw)((0,l.SU)(v)),1),(0,s.Wm)((0,l.SU)(U.Z),{inline:"",enableTimePicker:!1,monthChangeOnScroll:!1,modelValue:(0,l.SU)(v),"onUpdate:modelValue":[a[5]||(a[5]=e=>(0,l.dq)(v)?v.value=e:null),ae],autoApply:""},null,8,["modelValue"]),ee.value?((0,s.wg)(),(0,s.iD)("div",R,[(0,s._)("p",null,[(0,s.Uk)(" # Tasks: "),(0,s._)("span",Y,(0,i.zw)(ee.value),1)]),(0,s._)("p",null,[(0,s.Uk)(" # Completed tasks: "),(0,s._)("span",G,(0,i.zw)($.value),1)]),(0,s._)("p",null,[(0,s.Uk)(" # Not completed tasks: "),(0,s._)("span",X,(0,i.zw)(x.value),1)])])):(0,s.kq)("",!0)]),(0,s.Wm)(_,{class:"footer"})])}}};const ee=(0,v.Z)($,[["__scopeId","data-v-d79199f4"]]);var te=ee}}]);