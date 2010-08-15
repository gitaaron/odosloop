var DocString = {

    currentState : false,
    isFirst : true,
    init : function() {
        setTimeout('DocString.pollHref()',500);
    },

    // take two dicts, iterate over the first and ensure there is a matching val in the second
    objectsAreSame : function(oldO,newO) { 
        areSame = true;
        for (var val in newO) { 
            if(newO[val]!==oldO[val]) {
                areSame = false;
                break;
            }
        }
        return areSame;

    },
    // take two dicts, iterate over the new one and provide a diff of any that have changed
    getDiff : function(oldO,newO) {
        diff = {}
        for (var val in newO) {
            if (newO[val]!==oldO[val]) {
                diff[val] = newO[val];
            }
        } 
        return diff;
    },

    // poll the href and when it changes dispatch an event
    pollHref : function() {

        href = document.location.href;

        data = DocString.toDict(href);

        currentData = DocString.currentState;

        if (!currentData) {
            currentData = {};
        }
        diff = DocString.getDiff(currentData,data);
        if (!DocString.objectsAreSame(currentData,data)) {

            if (DocString.isFirst) {
                diff['isFirst'] = true;
            }
            DocString.currentState = data;
            $(document).trigger('hrefChanged', diff);

        } else if (DocString.isFirst) {

            diff['isFirst'] = true;
            $(document).trigger('hrefChanged', diff);
        }
        DocString.isFirst = false;
        setTimeout('DocString.pollHref()',500); 
    },

    // add data as dict of key value pairs to document location
    add : function(data) {
        currentVals = DocString.get();
        $.each(data, function(key,val) {
               currentVals[key] = val;
        });

        hash_str = DocString.toString(currentVals);

        new_href = document.location.href.split('#')[0] + hash_str;
        document.location.href = new_href;
    },

    // return all values as dict of key value pairs
    get : function() {
        return DocString.toDict(document.location.href);
    },    

    // take a dict and turn it into urlencoded string
    toString : function(data) {
        str = '';
        var isFirst = true;
        for (var key in data) {
            if (isFirst) {
                str += '#';
                isFirst = false;
            } else {
                str += '&';
            }
            str += key + '=' + data[key];
        }
        return str;
    },

    // take urlencoded href and return dict of key value pairs
    toDict : function(href) {
        href = href.split('#')[1]; 
        if(href) {
        key_vals = href.split('&');
        dict = {}
        for (i in key_vals) {
            key_val = key_vals[i];
            split = key_val.split('=');
            key = split[0];
            val = split[1];
            dict[key] = val;
        }
        return dict;
        } else {
            return {};
        }
    }


}
