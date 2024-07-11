//Create On 09/04/2021
//updated On 16/04/2021 - nested view fixed

function PrepareForm(formId,objectname, listData)
{
	var formElement = document.getElementById(formId);

	if(formElement == null)
	return;

	if(Array.isArray(listData))
	{
		var index = 0;
		for(var listObject in listData)
		{
			var  currentObject = listData[listObject];
			for(var field in currentObject)
			{
				if(!Array.isArray(field))
				{
					var newInput = document.createElement("input");
					newInput.id = objectname + "_" + field + "_" + index;
					newInput.name = objectname + "_" + field + "_" + index;
					newInput.type = "hidden";
					newInput.value = currentObject[field];
					formElement.appendChild(newInput);
				}
			}
			index++;
		}
		var newInput = document.createElement("input");
		newInput.id =  objectname + "_Count";
		newInput.name = objectname + "_Count";
		newInput.type = "hidden";
		newInput.value = listData.length;
		formElement.appendChild(newInput);
	}
	else
	{
		for(var field in listData)
		{
			if(!Array.isArray(listData[field]))
			{
				var newInput = document.createElement("input");
				newInput.id = objectname + "_" + field;
				newInput.name = objectname + "_" + field;
				newInput.type = "hidden";
				newInput.value = listData[field];
				formElement.appendChild(newInput);
			}
		}
	}
}

function Viewer(id, data, ajax=null)
{
    var _Viewer =
    {
        Id: id,
        Elements: null,
        Data: data,
		ResultNodes: null,
		ParentNode: null,
		PlaceHolder: null,
		RefreshData: false,
		BeforeNode: null,
		Template: new Array(),
		Intialized: false,
		Ajax: ajax,
		Nested: null,
		NestedElement: null
    };

    _Viewer.getNodeType = function (element)
    {
        var nodeType = -1;
		var tag = "";
        checkChildren = false;
		var isHtmlElement = false;

        if (element != null && element != undefined && element.nodeType != undefined)
            nodeType = element.nodeType;

        if (nodeType != 3 && nodeType != 4 && nodeType != 7 && nodeType != 8 && nodeType != 10 && nodeType != 12 && nodeType != -1)
		{
			if(element.tagName)
			tag = element.tagName;
            checkChildren = true;
			isHtmlElement = true;
		}

        if (element && element.length && element.length >= 0 && nodeType <= 0)
            checkChildren = true;
        else
            checkChildren = false;

        if (element.childNodes && element.childNodes.length && element.childNodes.length >= 0)
            checkChildren = true;
        else
            checkChildren = false;

        return { type: nodeType, name: tag ,hasChildren: checkChildren, isHtml: isHtmlElement };
    };

	_Viewer.Prepare = function(elementNode)
	{		
		var tagInfo = this.getNodeType(elementNode);
		
		var tagAttributes = new Array();
		
		var newElement = null;

		if(tagInfo.name && tagInfo.name != "")
			newElement = document.createElement(tagInfo.name);
		else if(tagInfo.type == 3 || tagInfo.type == 8)
			newElement = document.createTextNode(elementNode.nodeValue);

        if (elementNode.attributes != undefined && elementNode.attributes != null)
        for (var a = 0; a < elementNode.attributes.length;a++)
        {
            var attributeItem = elementNode.attributes[a];
            var plainText = attributeItem.nodeValue;
            var attributeName = attributeItem.nodeName;
			//tagAttributes.push({name : attributeName, value : plainText});
			newElement.setAttribute(attributeName, plainText);
        }


		var childElements = new Array();
		if(tagInfo.hasChildren)
		{
			for(var c=0;c<elementNode.childNodes.length;c++)
			{
				newElement.appendChild(this.Prepare(elementNode.childNodes[c]));
			}
		}
		
		return newElement;
	}
	
    _Viewer.Init = function ()
    {
        if(typeof(this.Id) == "string")
        {
            this.Elements = document.getElementById(this.Id);
			if(this.Elements == null)
				return false;
        }
        else
        {
            this.Elements = this.Id;
            this.Id = this.Id.id;
        }
		
		this.ParentNode = this.Elements.parentNode;
		this.BeforeNode = this.Elements.nextSibling;
		this.Template = this.Prepare(this.Elements);
		this.ParentNode.removeChild(this.Elements);
		this.Intialized =true;
		
		//check jquery presence for ajax
		if($ != null && $ != undefined)
		{
			if(this.Ajax != null && this.Ajax != undefined)
			{
				var thisRef = this;
				this.Ajax.success = function(response)
				{
					var loadedWith = false;
					if(typeof(response) == "string")
					{
						thisRef.Data = JSON.parse(response);
						thisRef.Process();
						loadedWith = true;
					}
					else
					{
						thisRef.Data = response;
						thisRef.Process();
						loadedWith = true;
					}
					if(loadedWith && thisRef.Ajax.onprocess)
					{
						thisRef.Ajax.onprocess(thisRef.Data);
					}
				};
				$.ajax(this.Ajax);
				return false;
			}
		}
		
		return true;
    };	


    _Viewer.hasAttribute = function (element, checkAttribute)
    {
        if (element != null && element != undefined && !element.getAttribute)
            return undefined;

        var elementSource = element.getAttribute(checkAttribute);
        if (elementSource != null && elementSource != "" && elementSource != undefined)
            return elementSource;

        return undefined;
    };

    _Viewer.applyValue = function (applyOn, text, refObject, rowindex, beforeBind, afterBind) {
        var boundText = "";
        var t = 0;

        var currentBounded = false;
        var plainText = text;

        if (plainText != "" && plainText != null && plainText != undefined) {
			var length = plainText.length;

            while (t < length) {
                if (plainText.substr(t, 2) == "{#") {
					t += 2;
					var startIndex = t;
					while(t < length)
					{
						if(plainText[t] == '}')
						{
							break;
						}
						t++;
					}
					var name = plainText.substr(startIndex, t-startIndex);
                    if (beforeBind != null)
                        beforeBind(name, refObject[name], attributeName);

					if(name == "srno")
						boundText += (rowindex + 1).toString();
					else if(name == "index")
						boundText += (rowindex).toString();
					else
	                    boundText += refObject[name];

					valueBinded = true;
                    currentBounded = true;
                    t++;
                }
                else if (plainText.substr(t, 3) == "{!#") {
					t += 3;
					var startIndex = t;
					var evalText = "";
					while(t < length)
					{
						if(plainText.substr(t, 2) == "{#")
						{
							var fieldname = "";
							var startIndex1 = t + 2;
							t += 2;
							while(t < length)
							{
								if(plainText[t] == '}')
								break;
								t++;
							}
							fieldname = plainText.substr(startIndex1, t - startIndex1);
							evalText += refObject[fieldname];
						}
						else if(plainText[t] == '}')
						{
							break;
						}
						else
						{
							evalText += plainText[t];
						}
						t++;
					}
					var result = eval(evalText);
					if(result != null && result != undefined)
					boundText += result.toString();
					t++;
                    valueBinded = true;
                    currentBounded = true;
				}
                else {
                    boundText += plainText.charAt(t).toString();
                    t++;
                }
            }
        }

        if (currentBounded) {
            applyOn.nodeValue = boundText;
            if (afterBind != null)
                afterBind(name, value, attributeName);
        }
        return currentBounded;
    };

    _Viewer.bindValue = function(element, refObject, rowindex, beforeBind, afterBind)
    {
        var valueBinded = false;
        var valueBindedCount = 0;

        if (element.attributes != undefined && element.attributes != null)
        for (var a = 0; a < element.attributes.length;a++)
        {
            var attributeItem = element.attributes[a];
            var plainText = attributeItem.nodeValue;
            var attributeName = attributeItem.nodeName;

            if(this.applyValue(attributeItem, plainText, refObject, rowindex, beforeBind, afterBind))
                valueBinded = true;
        }

        if (element.childNodes && element.childNodes.length > 0)
        {
            for (var n = 0; n < element.childNodes.length; n++) {
                if (element.childNodes[n].nodeType == 3) {
                    var attributeItem = element.childNodes[n];
                    var plainText = attributeItem.nodeValue;
                    var attributeName = "innerHtmlText";

                    if (this.applyValue(attributeItem, plainText, refObject, rowindex, beforeBind, afterBind))
                        valueBinded = true;
                }
            }
        }
        else
        {
            var attributeItem = element;
            var plainText = attributeItem.nodeValue;
            var attributeName = "innerHtmlText";
            if(this.applyValue(attributeItem, plainText, refObject, rowindex, beforeBind, afterBind))
                valueBinded = true;
        }

        return { IsBinded: valueBinded, Count: valueBindedCount };
    }
	

    _Viewer.foreachElement = function (element, refObject, rowindex=0, isnested)
    {
        var useObject = refObject;
        var nodeType = -1;
        var checkChildren = false;
		var iterationArray = new Array();


        var sourceData = this.hasAttribute(element, "datasource");
		
        var usingDataSource = false;
		var useIteration = false;
		
        if (sourceData != undefined && refObject != null && refObject != undefined) {
            useObject = refObject[sourceData];
            usingDataSource = true;
        }

        if (nestedData != undefined && !usingDataSource) {
			usingDataSource = true;
		}
		
		if(isnested)
			usingDataSource = true;
		
		if(Array.isArray(useObject) && usingDataSource)
		{
			var nodeInfo1 = this.getNodeType(element);
			
			var rtnList = new Array();
			var renderCount = 0;
			for(var x=0;x<useObject.length;x++)
			{
				if(useObject[x].id_delete && useObject[x].id_delete == "true")
				{
					//visiblity false
				}
				else
				{
					renderCount++;
					var newNode = element.cloneNode(true);
					newNode.removeAttribute("datasource");
					
					var index = 0;
					var limitChilds = newNode.childNodes.length;
	
					while(index < limitChilds)
					{
						var nestedData = this.hasAttribute(newNode.childNodes[index], "nestdata");
						var isEmpty = this.hasAttribute(newNode.childNodes[index], "empty");
						
						if(isEmpty != "" && isEmpty == "true")
						{
							newNode.removeChild(newNode.childNodes[index]);
							limitChilds--;
						}
						else
						{
							if (nestedData != undefined)
							{
								nestData = useObject[x][nestedData];
	
								var nestwithNode = element.cloneNode(true);
								nestwithNode.removeAttribute("datasource");
								
								var newNested = this.foreachElement(nestwithNode, nestData, 0, true);
								
								if(newNested.iteration && newNested.iteration.length > 0)
								{
									nestwithNode.removeAttribute("nested");
									
									var fixNestPosition= null;
									var limit = 0;
									var hasCurrentNode = false;
	
									while(limit < nestwithNode.childNodes.length)
									{
										if(nestwithNode.childNodes[limit].getAttribute && nestwithNode.childNodes[limit].getAttribute("nested") != "")
											fixNestPosition = nestwithNode.childNodes[limit];
										limit++;
									}
									
									if(fixNestPosition != null)
									while(fixNestPosition.childNodes.length > 0)
										fixNestPosition.removeChild(fixNestPosition.childNodes[0]);
									
									for(var n=0;n<newNested.iteration.length;n++)
									{
										var newcreated = newNested.iteration[n];
										newcreated.removeAttribute("nested");
										fixNestPosition.appendChild(newcreated);
									}
	
									newNode.appendChild(fixNestPosition);
								}
								else if(newNested.iteration == undefined)
								{
									newNode.appendChild(newNested);
								}
							}
							else
							{
								var updatedNode = this.foreachElement(newNode.childNodes[index], useObject[x], x, isnested);
								if(updatedNode.iteration == undefined)
									newNode.replaceChild(updatedNode, newNode.childNodes[index]);
								else
								{
									for(var element1 in updatedNode.iteration)
									{
										newNode.childNodes[index].appendChild(updatedNode.iteration[element1]);
									}
								}
							}
							index++;
						}
					}
					
					rtnList.push(newNode);
				}
			}
			
			if(renderCount == 0)
			{
				for(var i=0;i<element.childNodes.length; i++)
				{
					var isEmpty = this.hasAttribute(element.childNodes[i], "empty");
					if(isEmpty != "" && isEmpty == "true")
					{
						var newEmptyNode = element.childNodes[i].cloneNode(true);
						newEmptyNode.removeAttribute("empty");
						rtnList.push(newEmptyNode);
					}
				}
			}
			return {"iteration" : rtnList};
		}
		else
		{
			var nodeInfo1 = this.getNodeType(element);
			if (!nodeInfo1.hasChildren)
			{
				for (var attribute in useObject) {
					if (!Array.isArray(useObject[attribute]))
						this.bindValue(element, useObject, rowindex);
				}
			}
			else (nodeInfo1.hasChildren)
			{
				for (var attribute in useObject) {
					if (!Array.isArray(useObject[attribute]))
						this.bindValue(element, useObject, rowindex);
				}

				var i=0;
				while(i<element.childNodes.length)
				{
					var listItems = this.foreachElement(element.childNodes[i], useObject, rowindex, isnested);
					if(listItems.iteration)
					{
						var feedBefore = element.childNodes[i].nextSibling;
						if(listItems.iteration.length >= 0)
						{
							element.removeChild(element.childNodes[i]);
						}
					
						for(var d=0;d<listItems.iteration.length;d++)
						{
							element.insertBefore(listItems.iteration[d], feedBefore);
							i++;
						}
					}
					else
					{
						element.replaceChild(listItems, element.childNodes[i]);
					}
					i++;
				}
			}
		}

        return element;
    };
	
	_Viewer.Refresh = function(data)
	{
		if(!this.Intialized)
			return;
		
		if(data != undefined && data != null)
		this.Data = data;

		if(this.ResultNodes != null)
		{
			if(this.ResultNodes.length && this.ResultNodes.length > 0)
			{
				for(var i=0;i<this.ResultNodes.length; i++)
				this.PlaceHolder.removeChild(this.ResultNodes[i]);
			}
			else
			{
				this.PlaceHolder.removeChild(this.ResultNodes);
			}
			this.ResultNodes = null;
		}
		this.RefreshData = true;
		this.Process();
		this.RefreshData = false;
	};

	_Viewer.Process = function()
	{
		if(!this.Intialized)
			return;

		var newFragment = this.Template.cloneNode(true);
		
		if(newFragment.className != null && newFragment.className != "")
		newFragment.className = newFragment.className.replace(/\TemplateView\b/g, "");
		
		var resultItems = this.foreachElement(newFragment, this.Data);
		
		if(this.BeforeNode == null)
		{
			if(this.Elements != null)
			this.ParentNode.removeChild(this.Elements);
			this.ParentNode.appendChild(resultItems);
		}
		else
			this.ParentNode.insertBefore(resultItems, this.BeforeNode);

		this.PlaceHolder = this.ParentNode;
		this.ResultNodes = resultItems;
	};

    if(_Viewer.Init())
    _Viewer.Process();
    return _Viewer;
}

Viewer.Ready = null;

window.addEventListener("load", function (loadevent) {
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = ".TemplateView { display: none; }";
    document.getElementsByTagName('head')[0].appendChild(style);
	if(Viewer.Ready != null && Viewer.Ready != undefined)
		Viewer.Ready(loadevent);
});


//Ajax jquery functions

//Dropdown
AjaxDropDown.Items = new Array();

function AjaxDropDown(id, target, valuefield, displayfield, url, removeFirst=false)
{
	if((id !=undefined && id != null) && (target==undefined || target==null) && (valuefield==undefined || valuefield==null) && (displayfield == undefined || displayfield == null) && (url==undefined || url==null))
	{
		for(var x=0;x < AjaxDropDown.Items.length; x++)
		{
			if(AjaxDropDown.Items[x].id && AjaxDropDown.Items[x].id == id)
				return AjaxDropDown.Items[x].Item;
		}
		return null;
	}

	var _DropDown = {
		Url : url,
		Id : id,
		Target: target,
		ValueFields: valuefield,
		DisplayValues: displayfield,
		RemoveFirst: removeFirst,
		SelectedValue: null
	};

	_DropDown.Load = function(value, selectedvalue)
	{
		var refObject = this;
		if(selectedvalue == undefined && selectedvalue == null)
			selectedvalue = "";

		if(this.RemoveFirst == false)
			$("#"+this.Target).find('option').not(':first').remove();
		else
			$("#"+this.Target).find('option').remove();

		 $.ajax({
			url:this.Url+value,
			type:'get',
			dataType:'json',
			success:function (response) {
				var len = 0;
				if (response != null) {
					len = response.length;
				}
				
				if (len>0) {
					for (var i = 0; i<len; i++) {
						 var idText = response[i][refObject.ValueFields];
						 var labelText = response[i][refObject.DisplayValues];

						 var option = ""; 
						 if(selectedvalue.toString() == idText.toString())
						 {
							 option = "<option value='"+idText+"' selected='selected'>"+labelText+"</option>";
							 refObject.SelectedValue = idText;
						 }
						 else
							 option = "<option value='"+idText+"'>"+labelText+"</option>";

						 $("#"+refObject.Target).append(option);
					}
				}		
			}
		 });
	};

	_DropDown.Init = function()
	{
		if(this.Id != null && this.Id != undefined && this.Id != "")
		{
			var refObject = this;
			$("#" + this.Id).on("change", function () {
				var value = $(this).val();
				refObject.Load(value);
			});
		}
		else
		{
			this.Load("");
		}
		AjaxDropDown.Items.push({"id" : this.Target, "Item" : this});
	};
	
	_DropDown.Init();
	
	return _DropDown;
}

//Treeview Dropdown
TreeViewDropDown.Items = new Array();
TreeViewDropDown.Active = null;
TreeViewDropDown.Action = {};
TreeViewDropDown.Action.Removed = "Removed";
TreeViewDropDown.Action.Selected = "Selected";
TreeViewDropDown.Action.Cleared = "Cleared";

function TreeViewDropDown(id, values, data,multiselect, valuemeber, displaymember,onchange, cssNormal,cssHover)
{
	if((id !=undefined && id != null) && (values==undefined || values == null) && (data==undefined || data==null) && (valuemeber == undefined || valuemeber == null) && (displaymember==undefined || displaymember==null))
	{
		for(var x=0;x < TreeViewDropDown.Items.length; x++)
		{
			if(TreeViewDropDown.Items[x].id && TreeViewDropDown.Items[x].id == id)
				return TreeViewDropDown.Items[x].Item;
		}
		return null;
	}

	var foundElement = ((typeof(id)=="string")?document.getElementById(id):id);
	if(values != undefined && values != null && values == "" && foundElement != null && foundElement.value != "")
	values = foundElement.value;

	var _TreeViewDropDown = 
	{
		Element : foundElement,
		PlaceHolder : null,
		SelectionHolder: null,
		TypeTextBox : null,
		MultiSelect : multiselect,
		Selected : ((typeof(values) == "string" && values != "")?values.split(','):(Array.isArray(values)) ? values : new Array()),
		SelectedText : new Array(),
		ValueMember:valuemeber,
		DisplayMember: displaymember,
		ListItems : data,
		ViewListItems: new Array(),
		OnChange : onchange,
		CSSNormal:cssNormal,
		CSSHover: cssHover,
		Intialized : false,
		Searching: false,
		ListView: null
	};

	_TreeViewDropDown.IndexOf = function(value)
	{
		var i=0;
		while(i<this.ViewListItems.length)
		{
			if(this.ViewListItems[i].Value == value)
			{
				return i;
			}
			i++;
		}
		return -1;
	};

	_TreeViewDropDown.IsValueSelected = function(value)
	{
		var i=0;
		while(i<this.Selected.length)
		{
			if(this.Selected[i] == value)
			{
				return i;
			}
			i++;
		}
		return -1;
	};

	_TreeViewDropDown.MakeSelection = function(values, setvalues)
	{
		if(setvalues == undefined || setvalues == null)
		{
			if(Array.isArray(values))
			{
				if(!this.MultiSelect)
				{
					this.Selected = new Array();
					this.SelectedText = new Array();
					if(values.length > 0)
					this.Selected.push(values[0].toString());
				}
				else
				{
					for(var i=0;i<values.length;i++)
					{
						this.Selected.push(values[i].toString());
					}
				}
			}
			else
			{
				if(!this.MultiSelect)
				{
					this.Selected = new Array();
					this.SelectedText = new Array();
					this.Selected.push(values.toString());
				}
				else
				{
					this.Selected.push(values.toString());
				}
			}	
		}
		var newResult = document.createElement("div");
		this.Searching = false;
		for(var i=0;i<this.ListItems.length;i++)
		this.PrepareListItem(newResult, this.ListItems[i]);
		this.Searching = false;
	};

	_TreeViewDropDown.ClearSelection = function()
	{
		this.Selected = new Array();
		this.SelectedText = new Array();
		while(this.SelectionHolder.childNodes.length > 0)
		this.SelectionHolder.removeChild(this.SelectionHolder.childNodes[0]);

		if(this.Element != null)
		this.Element.value = "";

		if(this.OnChange != undefined && this.OnChange != null && this.OnChange != "")
		{
			this.OnChange("Cleared","");
		}
	};

	_TreeViewDropDown.RemoveItem = function(value)
	{
		var i=0;
		var newSelecteValues = "";
		while(i<this.Selected.length)
		{
			if(this.Selected[i] == value)
			{
				this.Selected.splice(i, 1);
			}
			else
			{
				newSelecteValues += this.Selected[i] + ",";
				i++;
			}
		}

		if(newSelecteValues != "")
		newSelecteValues = newSelecteValues.substr(0, newSelecteValues.length - 1);

		if(this.Element != null)
		this.Element.value = newSelecteValues;

		if(this.OnChange != undefined && this.OnChange != null && this.OnChange != "")
		{
			this.OnChange("Removed",value);
		}
	};

	_TreeViewDropDown.CreateSelection = function(divisionLabel)
	{
		var newSelection = divisionLabel.cloneNode(true);
		var refTreeNode = this;

		if(!this.MultiSelect && !this.Searching && this.Intialized)
		{
			this.ClearSelection();
		}

		while(newSelection.childNodes.length > 1)
		newSelection.removeChild(newSelection.childNodes[1]);

		newSelection.className = this.CSSHover;
		newSelection.style.width = "auto";
		newSelection.style.padding = "8px";
		newSelection.style.position = "relative";
		newSelection.style.borderRadius = "4px 4px";
		newSelection.style.margin = "8px";
		newSelection.style.float = "left";
		newSelection.style.cssFloat = "left";
		var removeAction = document.createElement("a");
		removeAction.style.backgroundColor = "#FF6666";
		removeAction.style.color = "white";
		removeAction.style.padding = "0px";
		removeAction.style.width = "20px"
		removeAction.style.height = "20px";
		removeAction.style.cssFloat = "right";
		removeAction.style.float = "right";
		removeAction.style.position = "relative";
		removeAction.style.textAlign = "center";
		removeAction.style.borderRadius = "3px 3px";
		removeAction.style.marginLeft = "8px";

		removeAction.appendChild(document.createTextNode("X"));
		removeAction.setAttribute("datavalue", newSelection.getAttribute("datavalue"));
		removeAction.addEventListener("click", function(){
			refTreeNode.RemoveItem(this.getAttribute("datavalue"));
			this.parentNode.parentNode.removeChild(this.parentNode);
		});
		newSelection.appendChild(removeAction);
		this.SelectionHolder.appendChild(newSelection, this.TypeTextBox);
	};

	_TreeViewDropDown.CreateListItem = function(parentTreeNode, listitem)
	{
		var divisionLabel = document.createElement("div");
		divisionLabel.style.padding = "8px";
		divisionLabel.style.borderBottom = "dotted 1px #eaeaea";

		var textClick = this.ValueMember;
		var textDisplay = this.DisplayMember;

		for(var field in listitem)
		{
			if(!Array.isArray(listitem[field]))
			{
				textClick = textClick.replace("#" + field + "#", listitem[field]);
				textDisplay = textDisplay.replace("#" + field + "#", listitem[field]);
			}
		}

		if(!this.Intialized)
		{
			this.ViewListItems.push({"Value":textClick, "Text":textDisplay});
		}

		if(this.Searching && textDisplay.toLowerCase().indexOf(this.TypeTextBox.value.toLowerCase()) < 0)
		{
			divisionLabel.style.display = "none";
		}
		else if(this.Searching)
		{
			parentTreeNode.style.display = "block";
			divisionLabel.style.display = "block";
		}

		var displayTextNode = document.createTextNode(textDisplay);
		var linkNode = document.createElement("a");
		linkNode.style.position = "relative";
		linkNode.style.width = "100%";
		linkNode.style.padding = "8px";
		linkNode.style.borderRadius = "4px 4px";
		linkNode.className = this.CSSNormal;
		linkNode.style.cursor = "pointer";
		linkNode.appendChild(displayTextNode);
		divisionLabel.appendChild(linkNode);
		divisionLabel.setAttribute("datavalue", textClick);
		linkNode.setAttribute("datavalue", textClick);

		var refTreeNode = this;

		linkNode.addEventListener("mousemove", function(){
			this.className = refTreeNode.CSSHover;
			this.style.color = "white";
		});

		linkNode.addEventListener("mouseout", function(){
			this.className = refTreeNode.CSSNormal;
			this.style.color = "#808080";
		});

		linkNode.addEventListener("click", function(){
			var selectedValues = "";
			refTreeNode.CreateSelection(this);

			refTreeNode.Selected.push(this.getAttribute("datavalue"));
			refTreeNode.SelectedText.push(this.childNodes[0].nodeValue);
			refTreeNode.TypeTextBox.value = "";
			refTreeNode.TypeTextBox.placeholder = "type text to search ...";
			refTreeNode.TypeTextBox.size = refTreeNode.TypeTextBox.placeholder.length + 1;

			for(var i=0;i<refTreeNode.Selected.length;i++)
			selectedValues += refTreeNode.Selected[i].toString() + ",";

			refTreeNode.Close();

			if(selectedValues != "")
			selectedValues = selectedValues.substr(0, selectedValues.length - 1);

			refTreeNode.Element.value = selectedValues;

			if(refTreeNode.OnChange != null && refTreeNode.OnChange != undefined && refTreeNode.OnChange != "")
			{
				refTreeNode.OnChange("Selected",this.getAttribute("datavalue"));
			}

			return false;
		});

		if(this.IsValueSelected(textClick) >= 0 && !this.Searching)
			this.CreateSelection(linkNode);
		return divisionLabel;
	};

	_TreeViewDropDown.PrepareListItem = function(parentTreeNode,listitem)
	{
		if(!Array.isArray(listitem))
		{
			var newTreeNode = this.CreateListItem(parentTreeNode, listitem);
			parentTreeNode.appendChild(newTreeNode);

			for(var field in listitem)
			{
				if(Array.isArray(listitem[field]))
				{
					var childItems = listitem[field];
					for(var i=0;i<childItems.length;i++)
					this.PrepareListItem(newTreeNode, childItems[i]);
				}
			}
		}
	};

	_TreeViewDropDown.Close = function()
	{
		if(this.ListView != null)
		{
			this.ListView.parentNode.removeChild(this.ListView);
			this.ListView = null;
		}
	};

	_TreeViewDropDown.Search = function()
	{
		var newResult = document.createElement("div");
		newResult.style.position = "absolute";
		newResult.style.zIndex = "99999999999";
		newResult.style.top = (this.SelectionHolder.parentOffsetTop + this.SelectionHolder.offsetTop + this.SelectionHolder.offsetHeight) + "px";
		newResult.style.left = (this.PlaceHolder.offsetLeft) + "px";
		newResult.style.backgroundColor = "white";
		newResult.style.padding = "10px";
		newResult.style.border = "solid 1px #CCCCCC";
		newResult.style.borderRadius = "3px 3px";
		newResult.style.width = this.PlaceHolder.offsetWidth + "px";
		newResult.style.minHeight = "300px";
		newResult.style.overflow = "auto";

		this.Searching = true;
		for(var i=0;i<this.ListItems.length;i++)
		this.PrepareListItem(newResult, this.ListItems[i]);
		this.Close();
		this.PlaceHolder.appendChild(newResult);
		if(newResult.offsetHeight > 300)
		newResult.style.height = "300px";

		this.ListView = newResult;
		this.Searching = false;
	}

	_TreeViewDropDown.init = function()
	{
		var refTreeNode = this;

		if(this.CSSNormal == null || this.CSSNormal == undefined || this.CSSNormal == "")
		this.CSSNormal = "treenode-item-normal";

		if(this.CSSHover == null || this.CSSHover == undefined || this.CSSHover == "")
		this.CSSHover = "treenode-item-hover";

		if(this.Element != null && this.Element != undefined && this.Element != "")
		{
			this.TypeTextBox = document.createElement("input");
			this.TypeTextBox.style.clear = "both";
			this.TypeTextBox.style.border = "none 0px white";
			this.TypeTextBox.style.outline = "none 0px";
			this.TypeTextBox.style.margin = "0px";
			this.TypeTextBox.placeholder = "type text to search ...";
			this.TypeTextBox.size = this.TypeTextBox.placeholder.length + 1;
			this.TypeTextBox.style.fontSize = "18px";
			this.TypeTextBox.addEventListener("keydown", function(){
				if(this.value.length == 0)
				{
					this.placeholder = "type text to search ...";
					this.size = this.placeholder.length + 1;
				}
				else
					this.size = this.value.length + 1;
			});
			this.TypeTextBox.addEventListener("keyup", function(){
				refTreeNode.Search();
				if(this.value.length == 0)
				{
					this.placeholder = "type text to search ...";
					this.size = this.placeholder.length + 1;
				}
				else
					this.size = this.value.length + 1;
			});
			this.Element.type = "hidden";
			this.PlaceHolder = this.Element.parentNode;
			this.PlaceHolder.style.clear = "both";
			this.PlaceHolder.appendChild(this.TypeTextBox);
			this.SelectionHolder = document.createElement("div");
			this.SelectionHolder.className = "form-group";

			this.PlaceHolder.insertBefore(this.SelectionHolder, this.TypeTextBox);

			this.PlaceHolder.addEventListener("click", function(){
				refTreeNode.TypeTextBox.focus();
				if(TreeViewDropDown.Active != null)
				TreeViewDropDown.Active.Close();
				TreeViewDropDown.Active = refTreeNode;
			});

			document.body.addEventListener("click", function(ev){
				if(TreeViewDropDown.Active != null && ev.target != TreeViewDropDown.Active.ListView && ev.target != TreeViewDropDown.Active.TypeTextBox)
				{
					TreeViewDropDown.Active.Close();
					TreeViewDropDown.Active = null;
				}
			});

			this.MakeSelection(this.Selected, false);

			TreeViewDropDown.Items.push({"id":this.Element.id,"Item":this});
			this.Intialized = true;
		}
	};

	_TreeViewDropDown.init();

	return _TreeViewDropDown;
}