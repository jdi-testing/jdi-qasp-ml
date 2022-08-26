
import {Component, Input} from '@angular/core';

/**
 * @title Stepper overview
 */
 @Component({
  selector: 'app-stepper',
  templateUrl: './stepper.component.html',
  styleUrls: ['./stepper.component.css']
})
export class StepperComponent {
  @Input() type?: number;
}
