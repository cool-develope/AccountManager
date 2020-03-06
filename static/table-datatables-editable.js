var TableDatatablesEditable = function () {

    var handleTable = function (nCnt, urlMap) {

        function restoreRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);

            for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                oTable.fnUpdate(aData[i], nRow, i, false);
            }

            oTable.fnDraw();
        }

        function editRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);
            for (var i = 0; i < nCnt; i++)
                jqTds[i].innerHTML = '<input type="text" class="form-control input-small" value="' + aData[i] + '">';
            jqTds[nCnt].innerHTML = '<a class="edit" href="">Save</a>';
            jqTds[nCnt + 1].innerHTML = '<a class="cancel" href="">Cancel</a>';
        }

        function saveRow(oTable, nRow) {
            var jqInputs = $('input', nRow);
            for (var i = 0; i < nCnt; i++) 
                oTable.fnUpdate(jqInputs[i].value, nRow, i, false);
            oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, nCnt, false);
            oTable.fnUpdate('<a class="delete" href="">Delete</a>', nRow, nCnt + 1, false);
            oTable.fnDraw();
        }

        function cancelEditRow(oTable, nRow) {
            var jqInputs = $('input', nRow);
            for (var i = 0; i < nCnt; i++)
                oTable.fnUpdate(jqInputs[i].value, i, 0, false);
            oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, nCnt, false);
            oTable.fnDraw();
        }

        var table = $('#editable_table');

        var oTable = table.dataTable({

            // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
            // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js). 
            // So when dropdowns used the scrollable div should be removed. 
            //"dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",

            "lengthMenu": [
                [5, 15, 20, -1],
                [5, 15, 20, "All"] // change per page values here
            ],

            // Or you can use remote translation file
            //"language": {
            //   url: '//cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese.json'
            //},

            // set the initial value
            "pageLength": 5,

            "language": {
                "lengthMenu": " _MENU_ records"
            },
            "columnDefs": [{ // set default column settings
                'orderable': true,
                'targets': [0]
            }, {
                "searchable": true,
                "targets": [0]
            }],
            "order": [
                [0, "asc"]
            ] // set first column as a default sort by asc
        });


        var nEditing = null;
        var nNew = false;

        table.on('click', '.delete', function (e) {
            e.preventDefault();

            if (confirm("Are you sure to delete this row ?") == false) {
                return;
            }

            var nRow = $(this).parents('tr')[0];
            var aData = oTable.fnGetData(nRow);
            oTable.fnDeleteRow(nRow);
            $.post(urlMap['delete'],
                {cur:aData[0], extra:aData[1]},
                function(data){});
        });

        table.on('click', '.cancel', function (e) {
            e.preventDefault();
            if (nNew) {
                oTable.fnDeleteRow(nEditing);
                nEditing = null;
                nNew = false;
            } else {
                restoreRow(oTable, nEditing);
                nEditing = null;
            }
        });

        table.on('click', '.edit', function (e) {
            e.preventDefault();
            nNew = false;
            
            /* Get the row as a parent of the link that was clicked on */
            var nRow = $(this).parents('tr')[0];

            if (nEditing !== null && nEditing != nRow) {
                /* Currently editing - but not this row - restore the old before continuing to edit mode */
                restoreRow(oTable, nEditing);
                editRow(oTable, nRow);
                nEditing = nRow;
            } else if (nEditing == nRow && this.innerHTML == "Save") {
                /* Editing this row and want to save it */
                var prevData = oTable.fnGetData(nRow);
                saveRow(oTable, nEditing);
                var curData = oTable.fnGetData(nRow);
                nEditing = null;
                $.post(urlMap['edit'],
                    {prev:prevData, cur:curData},
                    function(data) {});
            } else {
                /* No edit in progress - let's start one */
                editRow(oTable, nRow);
                nEditing = nRow;
            }
        });
    }

    return {

        //main function to initiate the module
        init: function (nCnt, urlMap) {
            handleTable(nCnt, urlMap);
        }

    };

}();