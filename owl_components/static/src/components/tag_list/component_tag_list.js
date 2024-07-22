/** @odoo-module **/
import { registry } from "@web/core/registry";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Component, useSubEnv, useState,useRef,onWillStart } from "@odoo/owl";
import { TagsList } from "@web/core/tags_list/tags_list";

export class TagListCustom extends Component {

static components={
  TagsList,
}
setup(){
  this.crmTagModel = 'crm.tag';
  this.orm = useService('orm');
   this.notification = useService('notification');
  this.state = useState({
     crm_tags:[],
  })

  onWillStart(async ()=>{
    await this.getCRMTags()
  })

}

async getCRMTags(){
   this.state.crm_tags = await this.orm.searchRead(this.crmTagModel,[],["id","name","color"]);
  }

  crmTags(){
    const tags = this.state.crm_tags;
    return Object.values(tags).map((tag)=>{
      const tag_value = Object.values(tag);

      return {
        id: tag_value[0],
        text: tag_value[1],
        colorIndex : tag_value[2],
        onDelete: (ev)=>this.tagOnDelete(ev),
        onClick: (ev)=> this.tagClicked(ev),
      }
    })
  }
  tagOnDelete(ev){
  console.log(ev);
  const badgetText = ev.target.closest('.badge').textContent.trim();
  const entries = Object.entries(this.state.crm_tags);
  const filtered= entries.filter(([key,value])=> value.name !== badgetText);
  this.state.crm_tags = Object.fromEntries(filtered);

  }

  tagClicked(ev){
    const clickedElement = ev.target;
    this.notification.add(
     "Has presionado " + clickedElement.textContent,
     {
     title:"Info",
     type: "info",
     sticky:true,
     }
    );
  }



}

TagListCustom.template = "owl.owl_tags_list";
registry.category("actions").add("owl.owl_tags_list", TagListCustom);