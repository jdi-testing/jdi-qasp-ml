import {Component, Input} from '@angular/core';

/**
 * @title Input with a clear button
 */
 @Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent {
  @Input() type?: number;
  value = 'Clear me';
}
