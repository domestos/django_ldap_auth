import React from 'react';
import 'primereact/resources/themes/nova-light/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

import axios from 'axios';
import { DataTable, Column } from 'primereact/datatable';
import { Button } from 'primereact/button';

export class CarService {
  getCarsSmall() {
    console.log(axios.get('http://localhost:99/api/v1/equipment/equipment/').then(res => res.data));
    return axios.get('http://localhost:99/api/v1/equipment/equipment/')
      .then(res => res.data);
  }












}

class App extends React.Component {




  constructor() {
    super();
    this.state = {};
    this.state = {
      globalFilter: null
    };
    this.carservice = new CarService();
    this.brandTemplate = this.brandTemplate.bind(this);
    this.colorTemplate = this.colorTemplate.bind(this);
    this.actionTemplate = this.actionTemplate.bind(this);
  }

  colorTemplate(rowData, column) {
    return <span style={{ color: rowData['color'] }}>{rowData['color']}</span>;
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
    this.carservice.getCarsSmall().then(data => this.setState({ cars: data }));
  }

  render() {
    var carCount = this.state.cars ? this.state.cars.length : 0;
    var header = <div className="p-clearfix" style={{ 'lineHeight': '1.87em' }}>List of Cars <Button icon="pi pi-refresh" style={{ 'float': 'right' }} /></div>;
    var footer = "There are " + carCount + ' cars';

    let cols = [
      { field: 'inventory_number', header: 'inventory_number', sortable: 'true' },
      { field: 'host_name', header: 'host_name', filterMatchMode: "contains" },
      { field: 'date_of_purchase', header: 'date_of_purchase' },
      { field: 'user.username', header: 'alias' },
      { field: 'user.first_name', header: 'first_name' },
      { field: 'user.last_name', header: 'last_name' }
    ];

    let dynamicColumns = cols.map((col, i) => {
      return <Column key={col.field} field={col.field} header={col.header} />;
    });

    return (
      <DataTable value={this.state.cars}
        header={header} footer={footer}
        globalFilter={this.state.globalFilter}
        paginator={true} rows={100} first={this.state.first} onPage={(e) => this.setState({ first: e.first })}
        sortField={this.state.sortField} sortOrder={this.state.sortOrder} onSort={(e) => this.setState({ sortField: e.sortField, sortOrder: e.sortOrder })}
      >
        {dynamicColumns}
      </DataTable>
    );
  }









}

export default App;
