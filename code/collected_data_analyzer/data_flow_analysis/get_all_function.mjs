import esprima from 'esprima'
import fs from 'fs';
import estraverse from 'estraverse';

/**
 * run: node ./get_all_function.mjs
 * function: extract all function call
 * some format cannot be detected, not fixed yet (only for extremely complicated cases)
 */

function begin() {
    var walk = function (dir) {
        var results = [];
        var list = fs.readdirSync(dir);
        list.forEach(function (file) {
            if (file != '.DS_Store') {
                file = dir + '/' + file;
                var stat = fs.statSync(file);
                if (stat && stat.isDirectory()) {
                    /* Recurse into a subdirectory */
                    results = results.concat(walk(file));
                } else {
                    /* Is a file */
                    results.push(file);
                }
            }
        });
        return results;
    }

    function traverse_file(dir,) {
        var js_file = walk(dir);

        js_file.forEach(function (p) {
            if (p.slice(-3) == ".js") {
                // console.log(p);
                // var output = p.slice(0, -3) + '_chrome_api.json'
                var input_file=p;
                var output_file=p.slice(0, -3) + '_api.json';
                var output_file_all=p.slice(0, -3) + '_allfunc.json';
                handle_ast_file(input_file,output_file,output_file_all,traverse)
                // handle_ast_file(p, output, traverse);
            }
            //console.error('finish one ext '+p);
        });
        
        return;
    }
    
    function handle_ast_file(input_file, output_file,output_file_all, traverse) {
        var data = fs.readFileSync(input_file, { encoding: 'utf-8' });

        try {
            var node = esprima.parseScript(data);

            var called_api = []
            var called_func=[]

            // traverse(node, called_api, handle_ast_node);
            traverse_get_normal_function(node, called_func);
            //console.log(called_api);
            if (fs.existsSync(output_file)) {
                fs.unlinkSync(output_file);
            }
            if (fs.existsSync(output_file_all)) {
                fs.unlinkSync(output_file_all);
            }
            fs.writeFileSync(output_file, JSON.stringify(called_api));
            fs.writeFileSync(output_file_all, JSON.stringify(called_func));
            success = success + 1;
            console.error(input_file)
            console.error(success);
        } catch (e) {
            console.error('skip a file' + input_file);
            console.error(e);
            failed = failed + 1;
        }

    }
    
    // not used
    // function traverse(node, called_api, handle_ast_node) {
    //     var parentChain = [];
    //     estraverse.traverse(node, {
    //         enter: (node, parent) => {
    //             parentChain.push(parent);
    //             handle_ast_node(node, called_api, parentChain);
    //         },
    //         leave: (node) => {
    //             parentChain.pop();
    //         }
    //     }
    //     );

    // }

    function traverse_get_normal_function(node, called_func){
        
        estraverse.traverse(node, {
            enter: (node) => {
                if (node.type == "CallExpression"){
                    var nextNode=node.callee
                    var funcName=""
                    if (nextNode.property!=null){
                        funcName=nextNode.property.name
                    }else{
                        funcName=nextNode.name
                        // console.log(nextNode);
                    }
                   // find a function call
                   while(nextNode.object != null){
                    if (nextNode.object.property !=null){
                        funcName=nextNode.object.property.name+'.'+funcName
                    }else{
                        if (nextNode.object.type=="ThisExpression"){
                            funcName='this.'+funcName
                        }else{
                            // if (nextNode.object.name==null){
                            //     console.log(nextNode.object)
                            // }
                           funcName=nextNode.object.name+'.'+funcName 
                        }
                        
                    }
                    nextNode=nextNode.object
                   } 
                //    if (funcName.charAt(-1)=='.'){
                //     funcName=funcName.substring(0,-2)
                //    }
                //    console.log("name of Func ", funcName);
                   called_func.push({"name":funcName, "arguments":'null'})
                }
            }
        })
    }

    // function handle_ast_node(node, called_api, parentChain) {

    //     // reached_node.push(node);
    //     // console.log("handle one node")
    //     try {
    //         var recallChain = [];
    //         var partFunc = node.name + ".";
    //         if (node.name == "chrome"|| node.name=="browser") {
    //             while (parentChain.length != 0) {
    //                 var parent = parentChain.pop();
    //                 recallChain.push(parent);
    //                 if (parent.type == "CallExpression") {
    //                     // reach the end
    //                     // console.log("length of chrome API " + recallChain.length);
    //                     // console.log("name of chrome API"+JSON.stringify(parent));
    //                     partFunc = partFunc.slice(0, -1);
    //                     // console.log("name of API ", partFunc);
    //                     called_api.push({ "name": partFunc, "arguments": parent.arguments })
    //                     break;
    //                 } else if (parent.type == "MemberExpression") {
    //                     partFunc = partFunc + parent.property.name + '.';

    //                 } else {
    //                     // unqualified
    //                     break;
    //                 }
    //                 // console.log("get inside " + JSON.stringify(parent));
    //             }
    //             while (recallChain.length != 0) {
    //                 parentChain.push(recallChain.pop());
    //             }
    //         } else {
    //             // console.log(parentChain.length);
    //         }


    //     } catch (e) {
    //         console.log(e);
    //     }

    // }
    function print_info() {
        console.log('failed' + failed);
        console.log('success' + success);
        return;
    }
    var success = 0;
    var failed = 0;

    // // print_info();
    traverse_file('./test_data', handle_ast_file);
    // print_info();

    // for single file test
    // var input_file="test_data/background.js";
    // var output_file="test_data/background_result.json";
    // var output_file_all="test_data/background_result_all.json"
    // handle_ast_file(input_file,output_file,output_file_all,traverse)

}

begin();
