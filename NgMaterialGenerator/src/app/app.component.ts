import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  structure?: any = {};

  constructor() {
    fetch('generationStructure.txt')
      .then((response) => response.text())
      .then((data) => {    
        this.structure = JSON.parse(data);
        console.log(this.structure);
      });
  }
  title = 'NgMaterialGenerator';
}
