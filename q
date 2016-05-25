[1mdiff --git a/project/static/js/project/budget_allocation_item.js b/project/static/js/project/budget_allocation_item.js[m
[1mindex 05a0b6b..852010b 100644[m
[1m--- a/project/static/js/project/budget_allocation_item.js[m
[1m+++ b/project/static/js/project/budget_allocation_item.js[m
[36m@@ -60,19 +60,20 @@[m [mfunction RowVM(row, vm) {[m
 [m
         for (i in vm.count) {[m
             self[vm.count[i]] = ko.observable();[m
[31m-            if (row.aid_name == vm.count[i]) {[m
[31m-                self[vm.count[i]](row.amount)[m
[31m-            }[m
         }[m
[32m+[m
         for (i in row.aid_amount) {[m
             if (row.aid_amount[i].aid_name == null){[m
                 if (self.goa_amount() == undefined) {[m
                     self.goa_amount(row.aid_amount[i].amount);[m
                 } else {[m
[31m-                    debugger[m
                     self.goa_amount(self.goa_amount() + row.aid_amount[i].amount)[m
                 }[m
             }[m
[32m+[m
[32m+[m[32m            console.log(row.aid_amount[i].aid_name)[m
[32m+[m[32m            console.log(vm.count[i])[m
[32m+[m
             if (row.aid_amount[i].aid_name == vm.count[i]) {[m
                 self[vm.count[i]](row.aid_amount[i].amount)[m
             }[m
