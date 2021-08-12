import { Component, Input } from '@angular/core';

/**
 * @title Badge overview
 */
@Component({
  selector: 'app-badge',
  templateUrl: './badge.component.html',
  styleUrls: ['./badge.component.css'],
})
export class BadgeComponent {
  @Input() type?: number;

  hidden = false;

  toggleBadgeVisibility() {
    this.hidden = !this.hidden;
  }
}
