namespace Checksum
{
    partial class CoreForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.hashLabel = new System.Windows.Forms.Label();
            this.footerLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // hashLabel
            // 
            this.hashLabel.BackColor = System.Drawing.Color.Transparent;
            this.hashLabel.Cursor = System.Windows.Forms.Cursors.Hand;
            this.hashLabel.Font = new System.Drawing.Font("Consolas", 10.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.hashLabel.Location = new System.Drawing.Point(12, 9);
            this.hashLabel.Name = "hashLabel";
            this.hashLabel.Size = new System.Drawing.Size(342, 142);
            this.hashLabel.TabIndex = 0;
            this.hashLabel.Text = "No checksum provided";
            this.hashLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.hashLabel.Click += new System.EventHandler(this.hashLabel_Click);
            // 
            // footerLabel
            // 
            this.footerLabel.Location = new System.Drawing.Point(12, 177);
            this.footerLabel.Name = "footerLabel";
            this.footerLabel.Size = new System.Drawing.Size(342, 23);
            this.footerLabel.TabIndex = 1;
            this.footerLabel.Text = "Copyright © 2017 Trinity Software";
            this.footerLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // CoreForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(366, 209);
            this.Controls.Add(this.footerLabel);
            this.Controls.Add(this.hashLabel);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "CoreForm";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Checksum";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label hashLabel;
        private System.Windows.Forms.Label footerLabel;
    }
}

