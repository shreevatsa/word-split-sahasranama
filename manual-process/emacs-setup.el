;; Preserve spaces when breaking lines.
(electric-indent-local-mode -1)

(defun my-move-numbered-line ()
  "Find the next line starting with a number, cut it, and paste it here after an '='.
If no such line is found, just insert '='."
  (interactive)
  (let ((start-point (point)))
    ;; Search forward for a line beginning with a number ('^[0-9]').
    ;; The 't' argument prevents an error if the search fails.
    (if (re-search-forward "^[0-9]" nil t)
        (progn
          ;; Go to the beginning of the found line.
          (beginning-of-line)
          ;; Kill the entire line including its newline.
          (kill-line 1)
          ;; Return to the original cursor position.
          (goto-char start-point)
          ;; Insert the '=' sign and yank the killed line.
          (insert "=")
          (yank))
      ;; If no numbered line was found, just insert the character.
      (insert "="))))

(global-set-key (kbd "=") #'my-move-numbered-line)
