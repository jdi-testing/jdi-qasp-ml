import { Component, Input } from '@angular/core';

/**
 * @title Basic buttons
 */
@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.css'],
})
export class ButtonComponent {
  @Input() type?: number;
}
