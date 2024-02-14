import { AfterContentInit, Component, OnInit } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";

@Component({
  selector: "app-snackbar",
  templateUrl: "./snackbar.component.html",
  styleUrls: ["./snackbar.component.css"],
})
export class SnackbarComponent implements OnInit, AfterContentInit {
  constructor(private _snackBar: MatSnackBar) {}

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

  ngOnInit(): void {}

  ngAfterContentInit(): void {
    this._snackBar.open('message', 'action');
  }
}
