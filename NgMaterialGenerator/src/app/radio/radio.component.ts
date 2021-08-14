import { Component, Input } from "@angular/core";

/**
 * @title Radios with ngModel
 */
@Component({
  selector: "app-radio",
  templateUrl: "./radio.component.html",
  styleUrls: ["./radio.component.css"],
})
export class RadioComponent {
  @Input() type?: number;
  favoriteSeason: string;
  seasons: string[] = ["Winter", "Spring", "Summer", "Autumn"];

  constructor() {
    this.favoriteSeason = "";
  }
}
