/**
 * Created by wrufesh on 10/4/16.
 */
var validityVm =  function (observableArray, modal_visibility, api_url, data) {
            var self = this;
            self.id = ko.observable();

            self.valid_from = ko.observable();
            self.note = ko.observable();

            if (data) {
                for (k in self) {
                    self[k](data[k])
                }
            }

            self.list = observableArray;
            // self.api_url = '/payroll/api/grade-scale-validity/';
            self.api_url = api_url;

            self.save = function () {
                App.showProcessing();
                // debugger;
                App.remotePost(
                    self.api_url,
                    JSON.parse(ko.toJSON({
                        id: self.id,
                        valid_from: self.valid_from,
                        note: self.note
                    })),
                    function (res) {
                        self.list.push(new validityVm(self.list, modal_visibility, self.api_url, res));
                        App.hideProcessing();
                        modal_visibility(false);
                        App.notifyUser(
                            'New validity added successfully',
                            'success'
                        );
                    },
                    function (err) {
                        var err_message = err.responseJSON.detail;
                        var error = App.notifyUser(
                            err_message,
                            'error'
                        );
                        App.hideProcessing();
                    }
                )

            };
            self.update = function () {
                App.showProcessing();
                // debugger;
                App.remotePut(
                    self.api_url + self.id() + "/",
                    JSON.parse(ko.toJSON({
                        id: self.id,
                        valid_from: self.valid_from,
                        note: self.note
                    })),
                    function (res) {
                        self.valid_from(res.valid_from);
                        self.note(res.note);
                        App.hideProcessing();
                        modal_visibility(false);
                        App.notifyUser(
                            'Validity updated successfully',
                            'success'
                        );
                    },
                    function (err) {
                        var err_message = err.responseJSON.detail;
                        var error = App.notifyUser(
                            err_message,
                            'error'
                        );
                        App.hideProcessing();
                    }
                )
            };
            self._delete = function () {
                App.showProcessing();
                App.remoteDelete(
                    self.api_url + self.id() + "/",
                    {},
                    function (res) {
                        self.list.remove(self);
                        App.hideProcessing();
                        modal_visibility(false);
                        App.notifyUser(
                            'Validity deleted successfully',
                            'success'
                        );
                    },
                    function (err) {
                        var err_message = err.responseJSON.detail;
                        var error = App.notifyUser(
                            err_message,
                            'error'
                        );
                        App.hideProcessing();
                    }
                )
            };

        };