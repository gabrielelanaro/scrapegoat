// Module to retrieve things from selenium
//# https://andreiglingeanu.me/nulify-transforms/

function nullifyTransforms(el) {
    const parseTransform = el =>
        window
            .getComputedStyle(el)
            .transform.split(/\(|,|\)/)
            .slice(1, -1)
            .map(v => parseFloat(v))

    // 1
    let { top, left, width, height } = el.getBoundingClientRect()
    let transformArr = parseTransform(el)

    if (transformArr.length == 6) {
        // 2D matrix
        const t = transformArr

        // 2
        let det = t[0] * t[3] - t[1] * t[2]

        // 3
        return {
            width: width / t[0],
            height: height / t[3],
            left: (left * t[3] - top * t[2] + t[2] * t[5] - t[4] * t[3]) / det,
            top: (-left * t[1] + top * t[0] + t[4] * t[1] - t[0] * t[5]) / det,
        }
    } else {
        // This case is not handled because it's very rarely needed anyway.
        // We just return the tranformed metrics, as they are, for consistency.
        return { top, left, width, height }
    }
}

var getAbsoluteBoundingBox = (node) => {
    // Get the bounding boxes the best that you can, and in an absolute
    // manner
    let box = nullifyTransforms(node);
    return {
        top: box.top + window.scrollY,
        bottom: box.top + box.height + window.scrollX,
        left: box.left + window.scrollY,
        right: box.left + box.width + window.scrollX
    }
};

var getPathTo = (element) => {
    if (element.tagName == 'HTML')
        return '/HTML[1]';
    if (element === document.body)
        return '/HTML[1]/BODY[1]';

    var ix = 0;
    var siblings = element.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {
        var sibling = siblings[i];
        if (sibling === element)
            return getPathTo(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
            ix++;
    }
}

const IGNORE_TAGS = ["script", "style", "title", "html", "body", "head"];

function getStyleFeatures(node) {
    let style = window.getComputedStyle(node);
    return {
        font: {
            family: style.fontFamily,
            size: style.fontSize,
            weight: style.fontWeight,
            style: style.fontStyle,
            variant: style.fontVariant,
        },
        color: style.color,
        border: style.border,
        background: { color: style.backgroundColor }
    }
}

var main = () => {
    // Annoying iframe
    Array.from(document.getElementsByTagName('iframe')).forEach((node) => node.remove());

    // Retrieve all elements
    var collection = document.getElementsByTagName("*");


    // Keep only own text
    collection = Array.from(collection)
        .filter((node) => (node.hasChildNodes()
            && !IGNORE_TAGS.includes(node.tagName.toLowerCase())
            && node.textContent.trim().length > 0)
        );
    return collection.map((node) => ({
        rect: getAbsoluteBoundingBox(node),
        node: node,
        text: node.childNodes[0].textContent.trim(),
        tag: node.tagName,
        style: getStyleFeatures(node),
        path: getPathTo(node)
    }));
};