import {Component} from '@angular/core';

/**
 * @title Expansion panel as accordion
 */
 @Component({
  selector: 'app-expansion-panel-accordion',
  templateUrl: './expansion-panel-accordion.component.html',
  styleUrls: ['./expansion-panel-accordion.component.css']
})
export class ExpansionPanelAccordionComponent {
  step = 0;

  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }
}
