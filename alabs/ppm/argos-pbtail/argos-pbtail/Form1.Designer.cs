namespace argos_pbtail
{
    partial class fmMain
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
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(fmMain));
            this.log1 = new System.Windows.Forms.Label();
            this.log2 = new System.Windows.Forms.Label();
            this.log3 = new System.Windows.Forms.Label();
            this.tm = new System.Windows.Forms.Timer(this.components);
            this.bgw1 = new System.ComponentModel.BackgroundWorker();
            this.bgw2 = new System.ComponentModel.BackgroundWorker();
            this.bgw3 = new System.ComponentModel.BackgroundWorker();
            this.pb1 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.pb1)).BeginInit();
            this.SuspendLayout();
            // 
            // log1
            // 
            this.log1.AutoEllipsis = true;
            this.log1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(242)))), ((int)(((byte)(242)))), ((int)(((byte)(242)))));
            this.log1.Font = new System.Drawing.Font("Segoe UI", 10.875F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.log1.ForeColor = System.Drawing.SystemColors.HotTrack;
            this.log1.Location = new System.Drawing.Point(133, 45);
            this.log1.Name = "log1";
            this.log1.Size = new System.Drawing.Size(1164, 62);
            this.log1.TabIndex = 2;
            this.log1.Text = "ARGOS RPA + Preparing STU and PAM or POT...";
            this.log1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.log1.UseCompatibleTextRendering = true;
            // 
            // log2
            // 
            this.log2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(242)))), ((int)(((byte)(242)))), ((int)(((byte)(242)))));
            this.log2.Font = new System.Drawing.Font("Segoe UI", 10.125F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.log2.ForeColor = System.Drawing.Color.CornflowerBlue;
            this.log2.Location = new System.Drawing.Point(127, 149);
            this.log2.Name = "log2";
            this.log2.Size = new System.Drawing.Size(1170, 62);
            this.log2.TabIndex = 3;
            this.log2.Text = "Processing ...";
            this.log2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // log3
            // 
            this.log3.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(242)))), ((int)(((byte)(242)))), ((int)(((byte)(242)))));
            this.log3.Font = new System.Drawing.Font("Segoe UI", 7.875F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.log3.ForeColor = System.Drawing.SystemColors.ControlDark;
            this.log3.Location = new System.Drawing.Point(128, 254);
            this.log3.Name = "log3";
            this.log3.Size = new System.Drawing.Size(1170, 68);
            this.log3.TabIndex = 4;
            this.log3.Text = "Starting ...";
            this.log3.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // tm
            // 
            this.tm.Interval = 1000;
            this.tm.Tick += new System.EventHandler(this.tm_Tick);
            // 
            // bgw1
            // 
            this.bgw1.DoWork += new System.ComponentModel.DoWorkEventHandler(this.bgw1_DoWork);
            // 
            // bgw2
            // 
            this.bgw2.WorkerSupportsCancellation = true;
            this.bgw2.DoWork += new System.ComponentModel.DoWorkEventHandler(this.bgw2_DoWork);
            // 
            // bgw3
            // 
            this.bgw3.WorkerSupportsCancellation = true;
            this.bgw3.DoWork += new System.ComponentModel.DoWorkEventHandler(this.bgw3_DoWork);
            // 
            // pb1
            // 
            this.pb1.Image = global::argos_pbtail.Properties.Resources.progressing;
            this.pb1.Location = new System.Drawing.Point(6, 123);
            this.pb1.Name = "pb1";
            this.pb1.Size = new System.Drawing.Size(114, 104);
            this.pb1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pb1.TabIndex = 5;
            this.pb1.TabStop = false;
            // 
            // fmMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(13F, 24F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(242)))), ((int)(((byte)(242)))), ((int)(((byte)(242)))));
            this.ClientSize = new System.Drawing.Size(1330, 371);
            this.Controls.Add(this.pb1);
            this.Controls.Add(this.log3);
            this.Controls.Add(this.log2);
            this.Controls.Add(this.log1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "fmMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pb1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Label log1;
        private System.Windows.Forms.Label log2;
        private System.Windows.Forms.Label log3;
        private System.Windows.Forms.Timer tm;
        private System.ComponentModel.BackgroundWorker bgw1;
        private System.ComponentModel.BackgroundWorker bgw2;
        private System.ComponentModel.BackgroundWorker bgw3;
        private System.Windows.Forms.PictureBox pb1;
    }
}

