import { Component } from '@angular/core';
import structure from '../generationStructure.json';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  structure?: any = {};

  constructor() {
    this.structure = structure;
  }
  title = 'NgMaterialGenerator';
}
