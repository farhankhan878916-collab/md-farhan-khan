import os
import zipfile

def package_project():
    project_dir = "movie-ticket-booking-system"
    zip_filename = "Movie-Ticket-Booking-System.zip"

    # Exclude heavy transient artifacts
    exclude_dirs = {"target", "node_modules", ".angular", ".git", ".idea", "__pycache__"}
    exclude_extensions = {".class", ".pyc", ".DS_Store"}

    print(f"Creating {zip_filename} from {project_dir}...")
    file_count = 0

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in exclude_extensions:
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                zipf.write(file_path, arcname)
                file_count += 1

    file_size_kb = os.path.getsize(zip_filename) / 1024
    print(f"Successfully created {zip_filename} with {file_count} files ({file_size_kb:.2f} KB).")

    # Also copy to public directory for direct download in preview app
    os.makedirs("public", exist_ok=True)
    import shutil
    shutil.copy(zip_filename, os.path.join("public", zip_filename))
    print(f"Copied to public/{zip_filename} for direct HTTP browser downloads.")

if __name__ == "__main__":
    package_project()
