function post(url, postData = {}) {
    return fetch({
        url,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    }).then(res => res.json())
}

function get(url) {
    return fetch(url).then(res => res.json())
}

function renderHeaderItem(data = {}) {
    let headerTemplate = '<li id="header-item-$id"><a href="#$id" class = "$isActive">$name</a></li>'
    Object.keys(data).forEach(key => {
        headerTemplate = headerTemplate.replaceAll('$' + key, data[key])
    })
    return headerTemplate
}


/**
 * 渲染头部列表
 */

function loadAndRenderHeader() {
    // 获取数据并渲染
    get('/subject').then(subjects => {
        const header = document.querySelector('.topmenu')
        const headerContent = subjects.map(renderHeaderItem).join('\n')
        header.innerHTML = headerContent
        console.log('[header] loaded!', headerContent)
    })
}


function renderSiderItem(data = {}) {
    let sideTemplate ='<a class="side-item-name-$id" onclick="loadAndRenderSubItem(event)">$name</a>' + '\n' +'<div class="item-content-$id"></div>'
    Object.keys(data).forEach(key => {
        sideTemplate = sideTemplate.replaceAll('$' + key, data[key])
    })
    return sideTemplate
}

/**
 * 渲染旁边列表
 */

function loadAndRenderSide() {
    // 获取数据并渲染
    get('/subject').then(subjects => {
        const sider = document.querySelector('.sidemenu')
        const siderContent = subjects.map(renderSiderItem).join('\n')
        sider.innerHTML = siderContent
        console.log('[sider] loaded!', siderContent)
    })
}

function renderSubSiderItem(data = {}) {
    let subsideTemplate ='<div class="sub-item-name-$id" onclick="loadAndRenderSubSubItem(event)">$name</div>' + '\n' + '<div class="sub-sub-content-name-$id"></div>'
    Object.keys(data).forEach(key => {
        subsideTemplate = subsideTemplate.replaceAll('$' + key, data[key])
    })
    return subsideTemplate
}

function loadAndRenderSubItem(evt) {
    const dom = evt.target
    var cont = dom.className;       
    console.log(dom.dataset)
    console.log(cont)
    const targetEle = dom.nextElementSibling
    get('/subsubject/'+ cont).then(subjects => {
        // const subsider = document.querySelector('.' + cont)
        const subsiderContent = subjects.map(renderSubSiderItem).join('\n')
        targetEle.innerHTML = subsiderContent
        console.log('[subsider] loaded!', subsiderContent)
    })
    
    // targetEle.innerHTML = new Array(10).fill(0).map(v => '<div class="sub-item">我是子类</div>').join('\n')
}

function renderSubSubSiderItem(data = {}) {
    let subsubsideTemplate ='<div class="sub-sub-item-name-$id" onclick="loadAndRenderCourseItem(event)">$name</div>' + '\n' + '<div class="sub-sub-sub-item-name-$id"></div>'
    Object.keys(data).forEach(key => {
        subsubsideTemplate = subsubsideTemplate.replaceAll('$' + key, data[key])
    })
    return subsubsideTemplate
}

function loadAndRenderSubSubItem(evt) {
    const dom = evt.target
    var cont = dom.className;       
    console.log(dom.dataset)
    console.log(cont)
    const targetEle = dom.nextElementSibling
    get('/subsubsubject/'+ cont).then(subjects => {
        // const subsider = document.querySelector('.' + cont)
        const subsubsiderContent = subjects.map(renderSubSubSiderItem).join('\n')
        targetEle.innerHTML = subsubsiderContent
        console.log('[subsubsider] loaded!', subsubsiderContent)
    })
    
    // targetEle.innerHTML = new Array(10).fill(0).map(v => '<div class="sub-item">我是子类</div>').join('\n')
}

function renderCourseItem(data = {}) {
    let courseTemplate ='<p class="course-$id"><b>$name</b><a style="color:rgb(66, 66, 66); font-size:13px;">  作者：$author   来源：$src</a></p>'
    Object.keys(data).forEach(key => {
        courseTemplate = courseTemplate.replaceAll('$' + key, data[key])
    })
    return courseTemplate
}

function loadAndRenderCourseItem(evt) {
    const dom = evt.target
    var cont = dom.className; 
    targetEle = document.getElementsByClassName("courselist")[0]
    console.log(targetEle.innerHTML)
    get('/course/'+ cont).then(subjects => {
        // const subsider = document.querySelector('.' + cont)
        const courseContent = subjects.map(renderCourseItem).join('\n')
        targetEle.innerHTML = courseContent
        console.log('[course] loaded!', courseContent)
    })
}

function init() {
    loadAndRenderHeader()
    loadAndRenderSide()
}

window.onload = init