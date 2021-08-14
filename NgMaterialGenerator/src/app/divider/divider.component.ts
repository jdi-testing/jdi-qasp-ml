
import {Component, Input} from '@angular/core';

/**
 * @title Basic divider
 */
 @Component({
  selector: 'app-divider',
  templateUrl: './divider.component.html',
  styleUrls: ['./divider.component.css']
})
export class DividerComponent {
  @Input() type?: number;
}
