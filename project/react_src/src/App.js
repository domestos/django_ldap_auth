import React from 'react';
import 'primereact/resources/themes/nova-light/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

import axios from 'axios';
import { Button } from 'primereact/button';

import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { MultiSelect } from 'primereact/multiselect';
export class CarService {
  getCarsSmall() {
    console.log("get data  from server getCarsSmall")
    // console.log(axios.get('http://localhost:99/api/v1/equipment/equipment/').then(res => res.data));
    return axios.get('http://localhost:99/api/v1/equipment/equipment/?format=json')
      .then(res => res.data);
  }

  getOnPage(page) {
    console.log("get data  from server getOnPage")
    console.log('http://localhost:99/api/v1/equipment/equipment/?format=api&page=' + page)

    if (page == 0)
      return axios.get('http://localhost:99/api/v1/equipment/equipment/?format=json')
        .then(res => res.data);
    else
      // console.log(axios.get('http://localhost:99/api/v1/equipment/equipment/').then(res => res.data));
      return axios.get('http://localhost:99/api/v1/equipment/equipment/?format=json&page=' + page)
        .then(res => res.data);
  }




  getGlobalSearch(value,page) {
    console.log("getGlobalSearch")
    console.log('http://localhost:99/api/v1/equipment/equipment/?search=' + value)
    console.log(axios.get('http://localhost:99/api/v1/equipment/equipment/?format=json&search=' + value+'&page=' + page)
    .then(res => res.data))

    if (page == 0)
    return axios.get('http://localhost:99/api/v1/equipment/equipment/?format=json&search=' + value)
      .then(res => res.data);
  else
    // console.log(axios.get('http://localhost:99/api/v1/equipment/equipment/').then(res => res.data));
    return axios.get('http://localhost:99/api/v1/equipment/equipment/?format=json&search=' + value+'&page=' + page)
      .then(res => res.data);
  }

}




class App extends React.Component {

  constructor() {
    super();
    let columns = [
      { field: 'inventory_number', header: 'inventory_number', sortable: 'true', filterElement: "brandFilter" },
      { field: 'host_name', header: 'host_name', filterMatchMode: "contains", filterElement: "brandFilter" },
      { field: 'date_of_purchase', header: 'date_of_purchase', filter: 'true', filterElement: "brandFilter" },
      { field: 'user.username', header: 'alias' },
      { field: 'user.first_name', header: 'first_name' },
      { field: 'user.last_name', header: 'last_name' }
    ];

    this.export = this.export.bind(this);

    this.colOptions = [];
    for (let col of columns) {
      this.colOptions.push({ label: col.header, value: col });
    }

    this.onColumnToggle = this.onColumnToggle.bind(this);


    this.state = {
      cars: [],
      cols: columns,
      loading: true,
      searchValue: '',
      globalFilter: null,
      first: 0,
      rows: 100,
      totalRecords: 0,
      previous: null,
      next: null

    };
    this.carservice = new CarService();
    this.brandTemplate = this.brandTemplate.bind(this);
    this.onRowEditorValidator = this.onRowEditorValidator.bind(this);
    this.actionTemplate = this.actionTemplate.bind(this);
    this.onBrandChange = this.onBrandChange.bind(this);
    this.onPage = this.onPage.bind(this);
    this.globalSearch = this.globalSearch.bind(this)
  }

  onPage(event) {
    console.log("onPage event", event.page);
    this.setState({
      loading: true
    });
    let val = this.state.searchValue
    //imitate delay of a backend call
    setTimeout(() => {
      this.carservice.getGlobalSearch(val, event.page).then(data => {
        this.setState({
          // totalRecords: data.length,
          cars: data.results,
          first: event.first,
          loading: false,
          totalRecords: data.count,
          next: data.next,
          previous: data.previous
          // cars: this.datasource.slice(0, this.state.rows),

        });
      });
    }, 1000);

  }





  globalSearch(event) {
    console.log("globalSearch event", event.target.value);
    this.setState({
      loading: true
    });
    let val = event.target.value
    // //imitate delay of a backend call
    setTimeout(() => {
      this.carservice.getGlobalSearch(val, 1).then(data => {
        this.setState({
          // totalRecords: data.length,
          cars: data.results,
          searchValue: val,
          loading: false,
          totalRecords: data.count,
          // next: data.next,
          // previous : data.previous
          // cars: this.datasource.slice(0, this.state.rows),

        });
      });
    }, 1000);

  }


  onBrandChange(event) {
    console.log(event);
    this.dt.filter(event.value, 'brand', 'equals');
    this.setState({ brand: event.value });
  }
  onColumnToggle(event) {
    this.setState({ cols: event.value });
  }

  export() {
    this.dt.exportCSV();
  }

  displaySelection(data) {
    if (!data || data.length === 0) {
      return <div style={{ textAlign: 'left' }}>No Selection</div>;
    }
    else {
      if (data instanceof Array)
        return <ul style={{ textAlign: 'left', margin: 0 }}>{data.map((car, i) => <li key={car.inventory_number}>{car.inventory_number + ' - ' + car.year + ' - ' + car.brand + ' - ' + car.color}</li>)}</ul>;
      else
        return <div style={{ textAlign: 'left' }}>Selected Car: {data.vin + ' - ' + data.year + ' - ' + data.brand + ' - ' + data.color}</div>
    }
  }

  onRowEditorValidator(rowData) {
    console.log(rowData)
    let value = rowData['brand'];
    return value.length > 0;
  }

  brandTemplate(rowData, column) {
    var src = "showcase/resources/demo/images/car/" + rowData.brand + ".png";
    return <img src={src} alt={rowData.brand} />;
  }

  actionTemplate(rowData, column) {
    return <div>
      <Button type="button" icon="pi pi-search" className="p-button-success"></Button>
      <Button type="button" icon="pi pi-pencil" className="p-button-warning"></Button>
    </div>;
  }
  componentDidMount() {
    setTimeout(() => {
      this.carservice.getCarsSmall().then(data => {

        this.setState({
          // totalRecords: data.length,
          cars: data.results,
          loading: false,
          totalRecords: data.count,
          next: data.next,
          previous: data.previous
          // cars: this.datasource.slice(0, this.state.rows),

        });
      });
    }, 1000);

    // this.carservice.getCarsSmall().then(data => this.setState({ cars: data }));
  }

  render() {

    let brands = [
      { label: 'All Brands', value: null },
      { label: 'Audi', value: 'Audi' },
      { label: 'BMW', value: 'BMW' },
      { label: 'Fiat', value: 'Fiat' },
      { label: 'Honda', value: 'Honda' },
      { label: 'Jaguar', value: 'Jaguar' },
      { label: 'Mercedes', value: 'Mercedes' },
      { label: 'Renault', value: 'Renault' },
      { label: 'VW', value: 'VW' },
      { label: 'Volvo', value: 'Volvo' }
    ];

    let brandFilter = <Dropdown style={{ width: '100%' }}
      value={this.state.brand} options={brands} onChange={this.onBrandChange} />


    var carCount = this.state.cars ? this.state.cars.length : 0;

    var footer = "There are " + carCount + ' cars';
    let header = <div style={{ textAlign: 'right' }}>
      <div style={{ 'textAlign': 'left' }}>
        <i className="pi pi-search" style={{ margin: '4px 4px 0 0' }}></i>
        <InputText type="search" onInput={this.globalSearch} placeholder="Global Search" size="50" />
        <Button type="button" icon="pi pi-external-link" iconPos="left" label="CSV" onClick={this.export}></Button>
      </div>

      <MultiSelect value={this.state.cols} options={this.colOptions} onChange={this.onColumnToggle} style={{ width: '250px' }} />


    </div>;

    let columns = this.state.cols.map((col, i) => {
      return <Column key={col.field} field={col.field} header={col.header} filter={true} sortable={true} />;
    });


    // let dynamicColumns = columns.map((col, i) => {
    //   return <Column key={col.field} field={col.field} header={col.header} />;
    // });

    return (
      <DataTable value={this.state.cars}
        rowEditorValidator={this.onRowEditorValidator}
        selectionMode="multiple" selection={this.state.selectedCars} onSelectionChange={e => this.setState({ selectedCars: e.value })} footer={this.displaySelection(this.state.selectedCars)}

        globalFilter={this.state.globalFilter}


        paginator={true} rows={this.state.rows} totalRecords={this.state.totalRecords} rowsPerPageOptions={[10, 50, 100]}
        lazy={true} first={this.state.first} onPage={this.onPage} loading={this.state.loading}
        //  paginator={true} rows={10} rowsPerPageOptions={[10,50,100]}first={this.state.first} onPage={(e) => this.setState({first: e.first})}
        loading={this.state.loading}
        ref={(el) => this.dt = el}
        value={this.state.cars} header={header}
        emptyMessage="No records found"
      >

        <Column selectionMode="multiple" />
        <Column field="inventory_number" header="inventory_number" filter={true} filterElement={brandFilter} />
        {columns}
        <Column rowEditor={true} style={{ 'width': '70px', 'textAlign': 'center' }}></Column>
        {/* {dynamicColumns} */}

      </DataTable>
    );
  }









}

export default App;
